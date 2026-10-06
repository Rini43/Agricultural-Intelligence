def callback(commit, metadata):
    if commit.author_email == b"gauthamsurendran21@gmail.com":
        commit.author_name = b"Rini43"
        commit.author_email = b"288579301+Rini43@users.noreply.github.com"

    if commit.committer_email == b"gauthamsurendran21@gmail.com":
        commit.committer_name = b"Rini43"
        commit.committer_email = b"288579301+Rini43@users.noreply.github.com"
