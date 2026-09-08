"""Bounded append-only protocol archives, with hashes rather than authenticity claims."""
from pathlib import Path
from . import __version__
from .bundle import BundleError, atomic_write, digest_file, source_digest
from .network_bundle import _json, _read

MAX_BYTES=512*1024*1024

def fresh(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    try:path.mkdir()
    except FileExistsError as exc:raise BundleError('output exists; preserve evidence and choose a fresh directory') from exc
    return path

def files(root):
    found={}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():raise BundleError('linked protocol artifacts are forbidden')
        if path.is_file():found[path.relative_to(root).as_posix()]=path
    if len(found)>1024 or sum(p.stat().st_size for p in found.values())>MAX_BYTES:raise BundleError('protocol archive budget exceeded')
    return found

def seal(root,kind):
    retained=files(root)
    manifest={'format':'earth-rehearsal-study-archive-v1','kind':kind,'version':__version__,'source_digest':source_digest(),'files':{name:{'bytes':path.stat().st_size,'sha256':digest_file(path)} for name,path in retained.items()}}
    _json(root/'archive.json',manifest)
    _json(root/'complete.json',{'format':'earth-rehearsal-study-complete-v1','kind':kind,'archive_sha256':digest_file(root/'archive.json')})

def verify(root,kind):
    root=Path(root);retained=files(root)
    if 'complete.json' not in retained or 'archive.json' not in retained:raise BundleError('incomplete protocol archive; retained attempts remain inspectable as files')
    c=_read(retained['complete.json']);m=_read(retained['archive.json'])
    if c!= {'format':'earth-rehearsal-study-complete-v1','kind':kind,'archive_sha256':digest_file(retained['archive.json'])}:raise BundleError('invalid protocol activation')
    if not isinstance(m,dict) or set(m)!= {'format','kind','version','source_digest','files'} or m['format']!='earth-rehearsal-study-archive-v1' or m['kind']!=kind or m['version']!=__version__:raise BundleError('protocol format/version mismatch')
    if not isinstance(m['source_digest'],str) or len(m['source_digest'])!=64 or any(v not in '0123456789abcdef' for v in m['source_digest']):raise BundleError('invalid protocol source identity')
    if not isinstance(m['files'],dict) or set(m['files'])!=set(retained)-{'archive.json','complete.json'}:raise BundleError('protocol artifact set mismatch')
    for name,entry in m['files'].items():
        if not isinstance(entry,dict) or set(entry)!= {'bytes','sha256'} or type(entry['bytes']) is not int or entry['bytes']!=retained[name].stat().st_size or entry['sha256']!=digest_file(retained[name]):raise BundleError('protocol artifact hash/size mismatch: '+name)
    return m

def export(root,target,kind,inspect):
    inspect(root);root=Path(root);target=fresh(target)
    for name,path in files(root).items():
        if name=='complete.json':continue
        (target/name).parent.mkdir(parents=True,exist_ok=True);atomic_write(target/name,path.read_bytes())
    atomic_write(target/'complete.json',(root/'complete.json').read_bytes())

def require_matching_source(manifest):
    if manifest['source_digest']!=source_digest():raise BundleError('source digest differs; use the exact matching source package to reproduce')
