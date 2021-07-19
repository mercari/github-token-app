import typer

from github_token_app.github_app import get_installations, get_read_token, get_write_pr_token, get_write_token

app = typer.Typer()

app.command(name="write")(get_write_token)
app.command(name="read")(get_read_token)
app.command(name="write-pr")(get_write_pr_token)
app.command(name="installations")(get_installations)


def main():
    app()


if __name__ == "__main__":
    main()
