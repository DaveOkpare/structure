import os
import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from utils import process_website

cwd = os.getcwd()


def main():
    print("\n[bold green]Welcome to the Structure CLI![/bold green]")
    print("[bold green]--------------------------------[/bold green]\n")

    website = typer.prompt("Please enter the website URL you want to scrape")
    print(f"Website to scrape: [bold green]{website}[/bold green]\n")

    extraction_target = typer.prompt("What would you like to extract from the website?")
    print(f"Data to extract: [bold green]{extraction_target}[/bold green]\n")

    num_items = typer.prompt("How many of them would you like to extract?")
    print(f"Number of items to extract: [bold green]{num_items}[/bold green]\n")

    fields = typer.prompt(
        "Enter the fields you want to organize the extracted data into (comma-separated)"
    )
    fields_list = [field.strip() for field in fields.split(",")]
    print(f"Fields to organize data: [bold green]{fields_list}[/bold green]\n")

    save_path = typer.prompt(
        "Where would you like to save the extracted data? (Please provide the file path)",
        default=cwd,
    )
    print("\n")
    file_name = "_".join(extraction_target.split(" ")) + ".json"
    save_path = os.path.join(save_path, file_name)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        output = process_website(
            url=website,
            prompt=f"Extract {num_items} {extraction_target} from the context",
            fields=fields_list,
        )
        with open(save_path, "w") as f:
            f.write(output)
        print(f"\nData saved to: [bold green]{save_path}[/bold green]")


if __name__ == "__main__":
    typer.run(main)
