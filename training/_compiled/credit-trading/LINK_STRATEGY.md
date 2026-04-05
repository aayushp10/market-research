# Link Strategy: current → v1.0

On Windows, `current/` is a full copy of `v1.0/` rather than a symlink or junction. This is the safer approach on Windows where symlinks require elevated privileges.

When the compile pipeline publishes a new version, it:
1. Writes the new version to `v<N>/`
2. Deletes the contents of `current/`
3. Copies the new version's contents into `current/`

The external publish step reads from `current/SKILL.md` regardless of implementation.
