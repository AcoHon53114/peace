#!/usr/bin/env python3
"""Read Vercel deployment metadata and compare public Pages snapshots; never mutate Vercel."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, quote, urlsplit
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def api(path, token, team, params=None):
    query = dict(params or {})
    if team:
        query['teamId'] = team
    url = 'https://api.vercel.com' + path + ('?' + urlencode(query) if query else '')
    # Disable redirects so the Authorization header cannot go to another host.
    from urllib.request import HTTPRedirectHandler, build_opener
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    try:
        with build_opener(NoRedirect).open(Request(url, headers={
            'Authorization': 'Bearer ' + token, 'User-Agent': 'Peace-Pages-Automation/1.0'
        }), timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f'Vercel metadata request failed (HTTP {exc.code}). Check token, project and team settings.') from None


def resolve(source, project, token, team='', fetch=api):
    bits = urlsplit(source)
    if bits.scheme != 'https' or not bits.hostname or bits.path not in ('', '/') or bits.query or bits.fragment or bits.username or bits.port:
        raise ValueError('PAGES_SOURCE must be an HTTPS origin without a path.')
    if not project.startswith('prj_') or not token:
        raise ValueError('Set PEACE_VERCEL_PROJECT_ID and the VERCEL_TOKEN Actions secret first.')
    alias = fetch('/v4/aliases/' + quote(bits.hostname, safe=''), token, team, {'projectId': project})
    if alias.get('projectId') != project or alias.get('redirect'):
        raise ValueError('The production domain is not assigned directly to the configured Vercel project.')
    deployment_id = alias.get('deploymentId')
    if not deployment_id or not re.fullmatch(r'dpl_[A-Za-z0-9]+', deployment_id):
        raise ValueError('The domain has no valid deployment ID.')
    deployment = fetch('/v13/deployments/' + deployment_id, token, team, {'withGitRepoInfo': 'true'})
    if deployment.get('id') != deployment_id or deployment.get('readyState') != 'READY' or deployment.get('target') != 'production':
        raise ValueError('The live domain does not point to a ready Production deployment; keeping the existing Pages site.')
    if deployment.get('projectId') and deployment['projectId'] != project:
        raise ValueError('Deployment project mismatch.')
    meta = deployment.get('meta') or {}
    sha = (deployment.get('gitSource') or {}).get('sha') or meta.get('githubCommitSha')
    if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('Cannot identify the deployed Git commit; do not mix main assets with another deployment.')
    repository = os.environ.get('GITHUB_REPOSITORY', 'AcoHon53114/peace').lower()
    if meta.get('githubCommitOrg') and meta.get('githubCommitRepo'):
        if (meta['githubCommitOrg'] + '/' + meta['githubCommitRepo']).lower() != repository:
            raise ValueError('Deployment belongs to a different Git repository.')
    return {'deployment_id': deployment_id, 'sha': sha, 'source': source.rstrip('/'), 'project_id': project}


def fingerprint(root):
    """Hash paths and bytes; normalize only the known news relative-age display."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.name == 'export-report.json':
            continue
        relative = path.relative_to(root).as_posix()
        payload = path.read_bytes()
        if path.suffix == '.html' and '/news/' in '/' + relative:
            soup = BeautifulSoup(payload, 'html.parser')
            for icon in soup.select('.custom-block-body > i.bi-calendar4'):
                sibling = icon.find_next_sibling()
                if sibling and sibling.name == 'span':
                    sibling.string = '[relative-publication-age]'
            payload = str(soup).encode()
        name = relative.encode()
        digest.update(len(name).to_bytes(8, 'big') + name + len(payload).to_bytes(8, 'big') + payload)
    return digest.hexdigest()


def output(name, value):
    filename = os.environ.get('GITHUB_OUTPUT')
    if filename:
        with open(filename, 'a') as stream:
            stream.write(f'{name}={value}\n')
    print(f'{name}: {value}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['resolve', 'verify', 'compare'])
    parser.add_argument('--state', default='.pages-state.json')
    parser.add_argument('--site', default='_site')
    parser.add_argument('--record', default='.pages-last/published.json')
    args = parser.parse_args()
    if args.command == 'compare':
        root = Path(args.site)
        report = json.loads((root / 'export-report.json').read_text())
        if report.get('warnings'):
            raise ValueError('Public images/files were unavailable. Keep the previous Pages site and retry later.')
        value = fingerprint(root)
        record = Path(args.record)
        previous = json.loads(record.read_text()) if record.exists() else {}
        changed = previous.get('fingerprint') != value
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps({'fingerprint': value}))
        output('changed', str(changed).lower())
        output('fingerprint', value)
        return
    state = resolve(os.environ.get('PAGES_SOURCE', 'https://peace-beta-sandy.vercel.app'),
                    os.environ.get('PEACE_VERCEL_PROJECT_ID', ''), os.environ.get('VERCEL_TOKEN', ''),
                    os.environ.get('PEACE_VERCEL_TEAM_ID', ''))
    path = Path(args.state)
    if args.command == 'verify':
        expected = json.loads(path.read_text())
        if state != expected:
            raise ValueError('Production changed during the export. Keeping Pages unchanged; the next event/hourly check will retry.')
        output('verified', 'true')
    else:
        path.write_text(json.dumps(state))
        output('sha', state['sha'])
        output('deployment_id', state['deployment_id'])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError) as exc:
        raise SystemExit(str(exc)) from None
