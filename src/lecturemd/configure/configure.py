from textual.app import App, ComposeResult
from textual import on
from textual.widgets import (
    Footer,
    Label,
    Markdown,
    TabbedContent,
    TabPane,
    Collapsible,
    Input,
    Static,
    Select,
    Switch,
    Button,
)
from textual.containers import (
    Vertical,
    Horizontal,
    Grid,
    VerticalScroll,
    Container,
    Center,
)
from textual.screen import ModalScreen


from typing import Callable, List, Tuple
from pathlib import Path

from typing import List
import yaml
from pathlib import Path
from copy import deepcopy

base_dir = Path(".").resolve()


class ConfirmationScreen(ModalScreen):
    
    def compose(self):
        with Container():
            yield Label("Are you sure?", classes = "title")
            yield Markdown("This will discard all changes you have made this session (*including those you've saved!*) and exit the configuration app.")
            with Horizontal():
                yield Button("Cancel", id = "modal_cancel", classes = "success")
                yield Button("Yes", id = "modal_yes", classes = "warning")


    @on(Button.Pressed)
    def handle_button(self, message):
        self.dismiss(message.button.id)

class FiltersDescriptionScreen(ModalScreen):
    def compose(self):
        with Container():
            yield Markdown(
"""
## Filters

Filters are applied in the order they are listed as Pandoc filters. A brief description of the in-built filters is given below.

----

- **combine_lists.py**: Combines lists which span multiple slides into a single list. A `div` with the class `combine-lists` which contains only multiple lists, separated by a horizontal rule (`---`), will be combined into a single list.
- **definitions.py**: Converts a markdown definition list into the correct format for the included `descriptions.sty` LaTeX package.
- **delistify.py**: Converts lists in the slides output to paragraphs in the notes output. 2nd order or higher lists are converted to 1st order (etc.) lists. 
- **examples.py**: Properly handles the formatting of examples in the beamer and revealjs output.
- **format_filter.py**: Filters content based on the output format. Any span or div with the class `html-only` will be removed from the latex output, and any span or div with the class `latex-only will be removed from the html output.
- **html_tcolorbox.py**: Converts markdown divs with the class `latex-env` and one of the classes `example`, `definitionbox`, or `aside` into tcolorbox equivalents in the html output.
- **latex-environment.py**: Converts markdown divs with the class `latex-env` into the correct LaTeX environment, and `latex-macro` into the correct LaTeX macro. For example, `[content]{.latex-macro .macro-name args="[opt-arg]{arg}"}` will be converted into `\macro-name[opt-arg]{arg}{content}`.
- **notesslides.py**: Filters content based on the output type. Any span or div with the class `notes-only` will be removed from the slides output (beamer and revealjs), and any span or div with the class `slides-only` will be removed from the notes output (pdf, html, and chunkedhtml).
- **pause_before.py**: Any span or div with the class `pause-before` will have an additional `\pause` command inserted before it in the beamer output (and equivalent for revealjs).
- **pandoc-crossref**: Adds cross-references to the output. See the [Pandoc Crossref documentation](https://lierdakil.github.io/pandoc-crossref/) for more information.
- **split_slides.py**: Allows multiple slides to occur within a div. A `div` with the class `split-on-slides` will be split into multiple slides, each containing a `div` with the same classes, attributes etc. as the original div.
- **tabularray.py**: Converts markdown tables into LaTeX tables using the `tabularray` package. This allows for more flexible table formatting.
""")
            with Horizontal():
                yield Button("Close", id = "modal_close", classes = "success")

    @on(Button.Pressed)
    def handle_button(self, message):
        self.dismiss(message.button.id)

class PostActionsDescriptionScreen(ModalScreen):
    def compose(self):
        with Container():
            yield Markdown(
"""
## Post Actions

Post actions are applied in the order they are listed. They should each be a python script which accepts a single command line argument: the ouput file (either a `.tex` or `.html` file). This file should then be modified in-place. These are useful for making final adjustments which would otherwise require the use of a custom Pandoc writer. However, if something is possible with a Pandoc filter, that should be the preferred option. A short list of the inbuilt post action files is given below.

----

- **tex_notes.py**: This performs three tasks:
    - Converts a `fixedfigure` environment containing a `figure` environment such that the position of the figure is `[H]` (i.e, fixed in the text instead of floating).
    - Converts equations which only contain a `split` environment into an `align*` environment.
    - Fixes some spacing around text subscripts and superscripts.
- **tex_slides.py**: This alters multi-line equations in an `align` environment to pause between each line. Note that this is not perfect -- generally, an extra pause is added after the first line of the equation, and the last line of an equation may appear at the same time as the next list item. This is due to Beamer's processing of an itemize environment with the `[<+->]` option.
""")
            with Horizontal():
                yield Button("Close", id = "modal_close", classes = "success")

    @on(Button.Pressed)
    def handle_button(self, message):
        self.dismiss(message.button.id)


def read_settings(base_dir: Path) -> dict:
    settings_path = base_dir / ".lecturemd/lecturemd.yaml"
    if not settings_path.exists():
        raise FileNotFoundError(
            f"""Settings file not found! 
Make sure you run this from the root of your lecturemd project.
I am looking for the settings file at .lecturemd/lecturemd.yaml.
I am running from here: {base_dir}
The full path to the settings file would be: {settings_path}"""
        )
    if not settings_path.is_file():
        raise FileNotFoundError("Settings file is not a file")
    with open(settings_path, "r") as f:
        settings = yaml.safe_load(f)

    settings["general"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["general"]["filters"]
    ]
    settings["latex"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["latex"]["filters"]
    ]
    settings["latex"]["notes"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["latex"]["notes"]["filters"]
    ]
    settings["latex"]["slides"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["latex"]["slides"]["filters"]
    ]
    settings["html"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["html"]["filters"]
    ]
    settings["html"]["notes"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["html"]["notes"]["filters"]
    ]
    settings["html"]["slides"]["filters"] = [
        {filter: 0} if isinstance(filter, str) else filter
        for filter in settings["html"]["slides"]["filters"]
    ]

    # Same for "post"

    settings["general"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["general"]["post"]
    ]
    settings["latex"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["latex"]["post"]
    ]
    settings["latex"]["notes"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["latex"]["notes"]["post"]
    ]
    settings["latex"]["slides"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["latex"]["slides"]["post"]
    ]
    settings["html"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["html"]["post"]
    ]
    settings["html"]["notes"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["html"]["notes"]["post"]
    ]
    settings["html"]["slides"]["post"] = [
        {post_action: 0} if isinstance(post_action, str) else post_action
        for post_action in settings["html"]["slides"]["post"]
    ]

    return settings


def write_settings(base_dir: Path, settings: dict):
    settings_path = base_dir / ".lecturemd/lecturemd.yaml"
    # settings_path = base_dir / "lecturemd.yaml"
    if not settings_path.exists():
        raise FileNotFoundError(
            """Settings file not found! 
Make sure you run this from the root of your lecturemd project.
I am looking for the settings file at .lecturemd/lecturemd.yaml."""
        )
    if not settings_path.is_file():
        raise FileNotFoundError(
            'Settings file ".lecturemd/lecturemd.yaml" is not a file.'
        )
    with open(settings_path, "w") as f:
        yaml.dump(settings, f)


settings = {}
original_settings = {}


settings_map = {}


def get_from_keys_list(d: dict, keys: List[str]) -> dict:
    for key in keys:
        d = d[key]
    return d


def set_from_keys_list(d: dict, keys: List[str], value):
    if len(keys) > 1:
        for key in keys[:-1]:
            d = d[key]
    d[keys[-1]] = value


def read_css(files: List[str | Path]) -> str:
    if isinstance(files, (str, Path)):
        files = [files]
    css = []
    for file in files:
        with open(Path(__file__).parent / file, "r") as f:
            css.append(f.read())
    return "\n".join(css)


def input_field(
    label: str,
    placeholder: str,
    value: str | None = None,
    id: str | None = None,
    keys: List[str] | None = None,
    callback: Callable | None = None,
    tooltip: str | None = None,
):
    global settings_map
    if keys is not None:
        if callback is not None:
            settings_map[id] = (keys, callback)
        else:
            settings_map[id] = keys
    if value is None and keys is not None:
        value = get_from_keys_list(settings, keys)
    label_widget = Label(label)
    if tooltip is not None:
        label_widget.tooltip = tooltip
        label_widget.add_class("tooltip")
    return Horizontal(
        label_widget,
        Input(placeholder=placeholder, value=value, id=id),
        classes="field",
    )


def select_field(
    label: str,
    options: list,
    initial: str | None = None,
    id: str | None = None,
    keys: List[str] | None = None,
    callback: Callable | None = None,
    tooltip: str | None = None,
):
    global settings_map
    if keys is not None:
        if callback is not None:
            settings_map[id] = (keys, callback)
        else:
            settings_map[id] = keys
    if initial is None and keys is not None:
        initial = get_from_keys_list(settings, keys)
    if not isinstance(options[0], (list, tuple)):
        options = [(s, s) for s in options]
    label_widget = Label(label)
    if tooltip is not None:
        label_widget.tooltip = tooltip
        label_widget.add_class("tooltip")
    return Horizontal(
        label_widget,
        Select(options=options, value=initial, id=id),
        classes="field tall",
    )


def switch_field(
    label: str,
    initial: bool = False,
    id: str | None = None,
    keys: List[str] | None = None,
    callback: Callable | None = None,
    tooltip: str | None = None,
):
    global settings_map
    if keys is not None:
        if callback is not None:
            settings_map[id] = (keys, callback)
        else:
            settings_map[id] = keys
    if initial is None and keys is not None:
        initial = get_from_keys_list(settings, keys)
    label_widget = Label(label)
    if tooltip is not None:
        label_widget.tooltip = tooltip
        label_widget.add_class("tooltip")
    return Horizontal(label_widget, Switch(value=initial, id=id), classes="field")


# region general settings


def general_settings():
    yield Label("These settings apply to all output formats.")
    yield input_field(
        "Main File",
        "main.md",
        id="main_file",
        keys=["general", "main file"],
        tooltip="The root file which is passed to Pandoc (or Pyndoc) for conversion.",
    )
    yield switch_field(
        "Use Pyndoc (Highly Recommended)",
        id="use_pyndoc",
        keys=["general", "use pyndoc"],
        initial=settings["general"][
            "use pyndoc"
        ],  # for some reason, getting from keys is not working, so we're doing it directly. Maybe something to do with bool conversion, but I couldn't find it.
        tooltip="Use Pyndoc and its preprocessor. See github.com/ech0-chambers/pyndoc for more information.",
    )
    yield from document_settings()
    yield from general_filters()
    yield from general_post_actions()
    yield from general_preambles()
    yield from maths_preamble()

def document_settings():
    with Collapsible(
        title="Document Settings", id="document_settings", collapsed=False
    ):
        yield input_field(
            "Title",
            "Your Title",
            id="title",
            keys=["general", "title"],
        )
        yield input_field(
            "Subtitle",
            "Your Subtitle",
            id="subtitle",
            keys=["general", "subtitle"],
        )
        yield input_field(
            "Author",
            "Your Name",
            id="author",
            keys=["general", "author"],
        )
        yield input_field(
            "Date",
            "Today",
            id="date",
            keys=["general", "date"],
            tooltip="Set to 'today' to automatically insert the current date at compile time.",
        )
        yield input_field(
            "Institution",
            "Your Institution",
            id="institution",
            keys=["general", "institution"],
            tooltip="The institution to be displayed in the footer.",
        )
        panel = Vertical(classes="panel")
        panel.border_title = "Logo"
        with panel:
            yield input_field(
                "Main Logo",
                "None",
                id="main_logo",
                keys=["general", "logo", "main logo"],
                tooltip="This is the logo which will appear on the cover of the pdf notes, and the header of the web notes. Leave blank for no logo.",
            )
            yield input_field(
                "Footer Logo",
                "None",
                id="footer_logo",
                keys=["general", "logo", "footer logo"],
                tooltip="This is the logo which will appear in the footer of the pdf and web notes. Leave blank for no logo.",
            )
        yield colour_scheme_picker()


def general_filters():
    filters = settings["general"]["filters"]
    yield from filters_panel(filters, "general", "general", None)
    return

def general_post_actions():
    post_actions = settings["general"]["post"]
    yield from post_actions_panel(post_actions, "general", "general", None)
    return

def filters_panel(
    filters: List[str | dict[str, int]],
    id_prefix: str,
    title: str,
    previous_filters: List[Tuple[str | dict[str, int], str]] | None = None,
    description: str | None = None,
    panel_title: str | None = None,
):
    all_filters = [
        (
            (filter, 0, None)
            if isinstance(filter, str)
            else (list(filter.keys())[0], list(filter.values())[0], None)
        )
        for filter in filters
    ]

    if previous_filters is not None:
        all_filters.extend(
            [
                (
                    (filter, 0, source)
                    if isinstance(filter, str)
                    else (list(filter.keys())[0], list(filter.values())[0], source)
                )
                for filter, source in previous_filters
            ]
        )

    all_filters.sort(key=lambda x: (x[1], "" if x[2] is None else x[2], x[0]))

    order_help_text = """Filters are applied starting with the lowest order number (which can be negative). If two filters have the same order, they are applied alphabetically by file name."""
    file_help_text = """The file to apply as a pandoc filter. This file must be executable (using `chmod +x` on linux). Filters which start with '$lecturemd' will be searched for in the lecturemd installation directory. All others are treated as a relative path."""

    if panel_title is None:
        panel_title = "Filters"

    with Collapsible(title=panel_title, id=f"{id_prefix}-filters", collapsed=True):
        if description is not None:
            yield Markdown(description)
        with Vertical(id=f"{id_prefix}-filters-grid", classes="filters-grid"):
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                order_label = Label("Order", classes="order tooltip")
                order_label.tooltip = order_help_text
                yield order_label
                yield Label("Remove", classes="remove")
            if len(all_filters) == 0:
                yield Label(
                    f"There are currently no filters applied to the {title} output.",
                    id=f"{id_prefix}-filters-none",
                )
            else:
                for filter in all_filters:
                    with Horizontal(
                        id=f"{id_prefix}-filter-{to_id_format(filter[0])}",
                        classes="row",
                    ):
                        yield Label(filter[0], classes="file")
                        yield Label(str(filter[1]), classes="order")
                        if filter[2] is not None:
                            yield Label(f"(from {filter[2]})", classes="source")
                        else:
                            yield Button(
                                "\U0001F5D1",
                                id=f"remove-{id_prefix}-filter-{to_id_format(filter[0])}",
                                classes="remove",
                            )
        panel_add_new = Vertical(
            id=f"{id_prefix}-filters-add-container", classes="filters-add-container"
        )
        panel_add_new.border_title = "Add New filter"
        with panel_add_new:
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                order_label = Label("Order", classes="order tooltip")
                order_label.tooltip = order_help_text
                yield order_label
                yield Label("Add", classes="add")
            with Horizontal(id=f"{id_prefix}-filters-add-horizontal", classes="row"):
                yield Input(
                    placeholder="filter.py",
                    id=f"{id_prefix}-filters-add",
                    classes="file",
                )
                yield Input(
                    placeholder="0",
                    value="0",
                    id=f"{id_prefix}-filters-add-order",
                    type="number",
                    classes="order",
                )
                yield Button("+", id=f"{id_prefix}-filters-add-button", classes="add")

        yield Button("Help", id=f"{id_prefix}-filters-help", classes="help")


def post_actions_panel(
    post_actions: List[str | dict[str, int]],
    id_prefix: str,
    title: str,
    previous_post_actions: List[Tuple[str | dict[str, int], str]] | None = None,
    description: str | None = None,
    panel_title: str | None = None,
):
    all_post_actions = [
        (
            (post_action, 0, None)
            if isinstance(post_action, str)
            else (list(post_action.keys())[0], list(post_action.values())[0], None)
        )
        for post_action in post_actions
    ]

    if previous_post_actions is not None:
        all_post_actions.extend(
            [
                (
                    (post_action, 0, source)
                    if isinstance(post_action, str)
                    else (list(post_action.keys())[0], list(post_action.values())[0], source)
                )
                for post_action, source in previous_post_actions
            ]
        )

    all_post_actions.sort(key=lambda x: (x[1], "" if x[2] is None else x[2], x[0]))

    order_help_text = """Post actions are applied starting with the lowest order number (which can be negative). If two post_actions have the same order, they are applied alphabetically by file name."""
    file_help_text = """The file to apply to the output file. This file must be executable (using `chmod +x` on linux), and will receive the file path to the output file as the only command line argument. They should read from this file, make changes to the content, then re-write to the same file. Post actions which start with '$lecturemd' will be searched for in the lecturemd installation directory. All others are treated as a relative path."""

    if panel_title is None:
        panel_title = "Post Actions"

    with Collapsible(title=panel_title, id=f"{id_prefix}-post-actions", collapsed=True):
        if description is not None:
            yield Markdown(description)
        with Vertical(id=f"{id_prefix}-post-actions-grid", classes="filters-grid"):
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                order_label = Label("Order", classes="order tooltip")
                order_label.tooltip = order_help_text
                yield order_label
                yield Label("Remove", classes="remove")
            if len(all_post_actions) == 0:
                yield Label(
                    f"There are currently no post_actions applied to the {title} output.",
                    id=f"{id_prefix}-post-actions-none",
                )
            else:
                for post_action in all_post_actions:
                    with Horizontal(
                        id=f"{id_prefix}-post-action-{to_id_format(post_action[0])}",
                        classes="row",
                    ):
                        yield Label(post_action[0], classes="file")
                        yield Label(str(post_action[1]), classes="order")
                        if post_action[2] is not None:
                            yield Label(f"(from {post_action[2]})", classes="source")
                        else:
                            yield Button(
                                "\U0001F5D1",
                                id=f"remove-{id_prefix}-post-action-{to_id_format(post_action[0])}",
                                classes="remove",
                            )
        panel_add_new = Vertical(
            id=f"{id_prefix}-post-actions-add-container", classes="filters-add-container"
        )
        panel_add_new.border_title = "Add New post_action"
        with panel_add_new:
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                order_label = Label("Order", classes="order tooltip")
                order_label.tooltip = order_help_text
                yield order_label
                yield Label("Add", classes="add")
            with Horizontal(id=f"{id_prefix}-post-actions-add-horizontal", classes="row"):
                yield Input(
                    placeholder="post_action.py",
                    id=f"{id_prefix}-post-actions-add",
                    classes="file",
                )
                yield Input(
                    placeholder="0",
                    value="0",
                    id=f"{id_prefix}-post-actions-add-order",
                    type="number",
                    classes="order",
                )
                yield Button("+", id=f"{id_prefix}-post-actions-add-button", classes="add")
        yield Button("Help", id=f"{id_prefix}-post-actions-help", classes="help")



def maths_preamble():
    preambles = settings["general"]["maths preamble"]
    description = """These preambles are applied to all output formats. For HTML (web) formats, these are encased in math mode for MathJax. For LaTeX (pdf) formats these are applied directly."""
    title = "Maths Preambles"
    yield from preambles_panel(
        preambles,
        "general-maths",
        "general maths",
        None,
        description=description,
        panel_title=title,
    )

def general_preambles():
    preambles = settings["general"]["preamble"]
    previous_preambles = settings["general"]["maths preamble"]
    previous_preambles = [
        (preamble, "general-maths") for preamble in previous_preambles
    ]
    yield from preambles_panel(
        preambles, "general", "general", previous_preambles=previous_preambles
    )
    return


def preambles_panel(
    preambles: List[str],
    id_prefix: str,
    title: str,
    previous_preambles: List[Tuple[str, str]] | None = None,
    description: str | None = None,
    panel_title: str | None = None,
):
    all_preambles = [(preamble, None) for preamble in preambles]
    if previous_preambles is not None:
        all_preambles.extend(
            [(preamble, source) for preamble, source in previous_preambles]
        )
    all_preambles.sort(key=lambda x: "" if x[1] is None else x[1])

    file_help_text = """The file to apply as a preamble. The file contents will be inserted into the headers of all output files."""

    if panel_title is None:
        panel_title = "Preambles"

    with Collapsible(title=panel_title, id=f"{id_prefix}-preambles", collapsed=True):
        if description is not None:
            yield Markdown(description)
        with Vertical(id=f"{id_prefix}-preambles-grid", classes="preambles-grid"):
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                yield Label("Remove", classes="remove")
            if len(preambles) == 0:
                yield Label(
                    f"There are currently no preambles applied to the {title} output.",
                    id=f"{id_prefix}-preambles-none",
                )
            else:
                for preamble in all_preambles:
                    with Horizontal(
                        id=f"{id_prefix}-preamble-{to_id_format(preamble[0])}",
                        classes="row",
                    ):
                        yield Label(preamble[0], classes="file")
                        if preamble[1] is not None:
                            yield Label(f"(from {preamble[1]})", classes="source")
                        else:
                            yield Button(
                                "\U0001F5D1",
                                id=f"remove-{id_prefix}-preamble-{to_id_format(preamble[0])}",
                                classes="remove",
                            )
        panel_add_new = Vertical(
            id=f"{id_prefix}-preambles-add-container", classes="preambles-add-container"
        )
        panel_add_new.border_title = "Add New preamble"
        with panel_add_new:
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                yield Label("Add", classes="add")
            with Horizontal(
                id=f"{id_prefix}-preambles-add-horizontal",
                classes="row preambles-add-horizontal",
            ):
                yield Input(
                    placeholder="preamble.tex",
                    id=f"{id_prefix}-preambles-add",
                    classes="file",
                )
                yield Button("+", id=f"{id_prefix}-preambles-add-button", classes="add")


def styles_panel(
    styles: List[str],
    id_prefix: str,
    title: str,
    previous_styles: List[Tuple[str, str]] | None = None,
    description: str | None = None,
    panel_title: str | None = None,
):
    all_styles = [(style, None) for style in styles]
    if previous_styles is not None:
        all_styles.extend([(style, source) for style, source in previous_styles])
    all_styles.sort(key=lambda x: "" if x[1] is None else x[1])

    file_help_text = """The file to apply as a linked stylesheet (css)."""

    if panel_title is None:
        panel_title = "Styles"

    with Collapsible(title=panel_title, id=f"{id_prefix}-styles", collapsed=True):
        if description is not None:
            yield Markdown(description)
        with Vertical(id=f"{id_prefix}-styles-grid", classes="styles-grid"):
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                yield Label("Remove", classes="remove")
            if len(styles) == 0:
                yield Label(
                    f"There are currently no styles applied to the {title} output.",
                    id=f"{id_prefix}-styles-none",
                )
            else:
                for style in all_styles:
                    with Horizontal(
                        id=f"{id_prefix}-style-{to_id_format(style[0])}",
                        classes="row",
                    ):
                        yield Label(style[0], classes="file")
                        if style[1] is not None:
                            yield Label(f"(from {style[1]})", classes="source")
                        else:
                            yield Button(
                                "\U0001F5D1",
                                id=f"remove-{id_prefix}-style-{to_id_format(style[0])}",
                                classes="remove",
                            )
        panel_add_new = Vertical(
            id=f"{id_prefix}-styles-add-container", classes="styles-add-container"
        )
        panel_add_new.border_title = "Add New style"
        with panel_add_new:
            with Horizontal(classes="header"):
                file_label = Label("File", classes="file tooltip")
                file_label.tooltip = file_help_text
                yield file_label
                yield Label("Add", classes="add")
            with Horizontal(
                id=f"{id_prefix}-styles-add-horizontal",
                classes="row styles-add-horizontal",
            ):
                yield Input(
                    placeholder="style.css",
                    id=f"{id_prefix}-styles-add",
                    classes="file",
                )
                yield Button("+", id=f"{id_prefix}-styles-add-button", classes="add")


# with open(Path(__file__).parent / "schemes.txt", "r") as f:
#     schemes = f.read().split("\n")
# schemes = [s for s in schemes if s]
from pygmentation import list_schemes, get_available_schemes

schemes = list_schemes(True, "^[^(slide)].*", get_available_schemes(), False)


def colour_scheme_picker():
    return select_field(
        "Colour Scheme",
        schemes,
        id="colour_scheme",
        keys=["general", "colour scheme"],
        tooltip="Select the colour scheme for the document. For information on how these colour schemes are defined and used, see github.com/ech0-chambers/pygmentation",
    )


# endregion

# region latex settings


def latex_settings():
    with TabbedContent(initial="latex_all"):
        with TabPane("All", id="latex_all"):
            yield from latex_all_settings()
        with TabPane("Notes", id="latex_notes"):
            yield from latex_notes_settings()
        with TabPane("Slides", id="latex_slides"):
            yield from latex_slides_settings()


# region latex all settings


def latex_all_settings():
    yield Label("These settings apply to all LaTeX (pdf) output formats.")
    yield input_field(
        "Default Image Format",
        "pdf",
        id="latex_figure_extension",
        keys=["latex", "figure extension"],
        callback=lambda x: x.lower().lstrip("."),
        tooltip="The default image format for figures. This is ignored for individual figures with a specified format.",
    )
    yield from latex_filters()
    yield from latex_post_actions()
    yield from latex_preambles()


def latex_filters():
    filters = settings["latex"]["filters"]
    previous_filters = settings["general"]["filters"]
    previous_filters = [(filter, "general") for filter in previous_filters]
    yield from filters_panel(
        filters,
        "latex",
        "LaTeX (pdf)",
        previous_filters,
        panel_title="LaTeX (pdf) Filters",
    )

def latex_post_actions():
    post_actions = settings["latex"]["post"]
    previous_post_actions = settings["general"]["post"]
    previous_post_actions = [(post_action, "general") for post_action in previous_post_actions]
    yield from post_actions_panel(
        post_actions,
        "latex",
        "LaTeX (pdf)",
        previous_post_actions,
        panel_title="LaTeX (pdf) post-actions",
    )

def latex_preambles():
    preambles = settings["latex"]["preamble"]
    previous_preambles = settings["general"]["preamble"]
    previous_preambles = [(preamble, "general") for preamble in previous_preambles]
    yield from preambles_panel(
        preambles,
        "latex",
        "LaTeX (pdf)",
        previous_preambles,
        panel_title="LaTeX (pdf) Preambles",
    )


# endregion

# region latex notes settings


def latex_notes_settings():
    yield Label("These settings apply to the LaTeX (pdf) notes output format.")
    yield from latex_notes_filters()
    yield from latex_notes_post_actions()
    yield from latex_notes_preambles()


def latex_notes_filters():
    filters = settings["latex"]["notes"]["filters"]
    latex_filters = settings["latex"]["filters"]
    general_filters = settings["general"]["filters"]
    latex_filters = [(filter, "latex") for filter in latex_filters]
    general_filters = [(filter, "general") for filter in general_filters]
    previous_filters = latex_filters + general_filters
    yield from filters_panel(
        filters,
        "latex-notes",
        "LaTeX (pdf) notes",
        previous_filters,
        panel_title="LaTeX (pdf) Notes Filters",
    )


def latex_notes_post_actions():
    post_actions = settings["latex"]["notes"]["post"]
    latex_post_actions = settings["latex"]["post"]
    general_post_actions = settings["general"]["post"]
    latex_post_actions = [(post_action, "latex") for post_action in latex_post_actions]
    general_post_actions = [(post_action, "general") for post_action in general_post_actions]
    previous_post_actions = latex_post_actions + general_post_actions
    yield from post_actions_panel(
        post_actions,
        "latex-notes",
        "LaTeX (pdf) notes",
        previous_post_actions,
        panel_title="LaTeX (pdf) Notes post-actions",
    )


def latex_notes_preambles():
    preambles = settings["latex"]["notes"]["preamble"]
    latex_preambles = settings["latex"]["preamble"]
    general_preambles = settings["general"]["preamble"]
    latex_preambles = [(preamble, "latex") for preamble in latex_preambles]
    general_preambles = [(preamble, "general") for preamble in general_preambles]
    previous_preambles = latex_preambles + general_preambles
    yield from preambles_panel(
        preambles,
        "latex-notes",
        "LaTeX (pdf) notes",
        previous_preambles,
        panel_title="LaTeX (pdf) Notes Preambles",
    )


# endregion

# region latex slides settings


def latex_slides_settings():
    yield Label("These settings apply to the LaTeX (pdf) slides output format.")
    yield from latex_slides_filters()
    yield from latex_slides_post_actions()
    yield from latex_slides_preambles()


def latex_slides_filters():
    filters = settings["latex"]["slides"]["filters"]
    latex_filters = settings["latex"]["filters"]
    general_filters = settings["general"]["filters"]
    latex_filters = [(filter, "latex") for filter in latex_filters]
    general_filters = [(filter, "general") for filter in general_filters]
    previous_filters = latex_filters + general_filters
    yield from filters_panel(
        filters,
        "latex-slides",
        "LaTeX (pdf) slides",
        previous_filters,
        panel_title="LaTeX (pdf) Slides Filters",
    )


def latex_slides_post_actions():
    post_actions = settings["latex"]["slides"]["post"]
    latex_post_actions = settings["latex"]["post"]
    general_post_actions = settings["general"]["post"]
    latex_post_actions = [(post_action, "latex") for post_action in latex_post_actions]
    general_post_actions = [(post_action, "general") for post_action in general_post_actions]
    previous_post_actions = latex_post_actions + general_post_actions
    yield from post_actions_panel(
        post_actions,
        "latex-slides",
        "LaTeX (pdf) slides",
        previous_post_actions,
        panel_title="LaTeX (pdf) Slides post-actions",
    )


def latex_slides_preambles():
    preambles = settings["latex"]["slides"]["preamble"]
    latex_preambles = settings["latex"]["preamble"]
    general_preambles = settings["general"]["preamble"]
    latex_preambles = [(preamble, "latex") for preamble in latex_preambles]
    general_preambles = [(preamble, "general") for preamble in general_preambles]
    previous_preambles = latex_preambles + general_preambles
    yield from preambles_panel(
        preambles,
        "latex-slides",
        "LaTeX (pdf) slides",
        previous_preambles,
        panel_title="LaTeX (pdf) Slides Preambles",
    )


# endregion


# endregion

# region html settings


def html_settings():
    with TabbedContent(initial="html_all"):
        with TabPane("All", id="html_all"):
            yield from html_all_settings()
        with TabPane("Notes", id="html_notes"):
            yield from html_notes_settings()
        with TabPane("Slides", id="html_slides"):
            yield from html_slides_settings()


# region html all settings


def html_all_settings():
    yield Label("These settings apply to all html (web) output formats.")
    yield input_field(
        "Default Image Format",
        "svg",
        id="html_figure_extension",
        keys=["html", "figure extension"],
        callback=lambda x: x.lower().lstrip("."),
        tooltip="The default image format for figures. This is ignored for individual figures with a specified format.",
    )
    yield from html_styles()
    yield from html_filters()
    yield from html_post_actions()
    yield from html_preambles()


def html_styles():
    styles = settings["html"]["styles"]
    yield from styles_panel(
        styles, "html", "html (web)", None, panel_title="HTML (web) Styles"
    )


def html_filters():
    filters = settings["html"]["filters"]
    previous_filters = settings["general"]["filters"]
    previous_filters = [(filter, "general") for filter in previous_filters]
    yield from filters_panel(
        filters,
        "html",
        "html (web)",
        previous_filters,
        panel_title="HTML (web) Filters",
    )


def html_post_actions():
    post_actions = settings["html"]["post"]
    previous_post_actions = settings["general"]["post"]
    previous_post_actions = [(post_action, "general") for post_action in previous_post_actions]
    yield from post_actions_panel(
        post_actions,
        "html",
        "html (web)",
        previous_post_actions,
        panel_title="HTML (web) post-actions",
    )


def html_preambles():
    preambles = settings["html"]["preamble"]
    previous_preambles = settings["general"]["preamble"]
    previous_preambles = [(preamble, "general") for preamble in previous_preambles]
    yield from preambles_panel(
        preambles,
        "html",
        "html (web)",
        previous_preambles,
        panel_title="HTML (web) Preambles",
    )


# endregion

# region html notes settings


def html_notes_settings():
    yield Label("These settings apply to the html (web) notes output format.")
    yield from html_notes_styles()
    yield from html_notes_filters()
    yield from html_notes_post_actions()
    yield from html_notes_preambles()


def html_notes_styles():
    styles = settings["html"]["notes"]["styles"]
    html_styles = settings["html"]["styles"]
    html_styles = [(style, "html") for style in html_styles]
    yield from styles_panel(
        styles,
        "html-notes",
        "html (web) notes",
        html_styles,
        panel_title="HTML (web) Notes Styles",
    )


def html_notes_filters():
    filters = settings["html"]["notes"]["filters"]
    html_filters = settings["html"]["filters"]
    general_filters = settings["general"]["filters"]
    html_filters = [(filter, "html") for filter in html_filters]
    general_filters = [(filter, "general") for filter in general_filters]
    previous_filters = html_filters + general_filters
    yield from filters_panel(
        filters,
        "html-notes",
        "html (web) notes",
        previous_filters,
        panel_title="HTML (web) Notes Filters",
    )


def html_notes_post_actions():
    post_actions = settings["html"]["notes"]["post"]
    html_post_actions = settings["html"]["post"]
    general_post_actions = settings["general"]["post"]
    html_post_actions = [(post_action, "html") for post_action in html_post_actions]
    general_post_actions = [(post_action, "general") for post_action in general_post_actions]
    previous_post_actions = html_post_actions + general_post_actions
    yield from post_actions_panel(
        post_actions,
        "html-notes",
        "html (web) notes",
        previous_post_actions,
        panel_title="HTML (web) Notes post-actions",
    )


def html_notes_preambles():
    preambles = settings["html"]["notes"]["preamble"]
    html_preambles = settings["html"]["preamble"]
    general_preambles = settings["general"]["preamble"]
    html_preambles = [(preamble, "html") for preamble in html_preambles]
    general_preambles = [(preamble, "general") for preamble in general_preambles]
    previous_preambles = html_preambles + general_preambles
    yield from preambles_panel(
        preambles,
        "html-notes",
        "html (web) notes",
        previous_preambles,
        panel_title="HTML (web) Notes Preambles",
    )


# endregion

# region html slides settings


def html_slides_settings():
    yield Label("These settings apply to the html (web) slides output format.")
    yield from html_slides_styles()
    yield from html_slides_filters()
    yield from html_slides_post_actions()
    yield from html_slides_preambles()


def html_slides_styles():
    styles = settings["html"]["slides"]["styles"]
    html_styles = settings["html"]["styles"]
    html_styles = [(style, "html") for style in html_styles]
    yield from styles_panel(
        styles,
        "html-slides",
        "html (web) slides",
        html_styles,
        panel_title="HTML (web) Slides Styles",
    )


def html_slides_filters():
    filters = settings["html"]["slides"]["filters"]
    html_filters = settings["html"]["filters"]
    general_filters = settings["general"]["filters"]
    html_filters = [(filter, "html") for filter in html_filters]
    general_filters = [(filter, "general") for filter in general_filters]
    previous_filters = html_filters + general_filters
    yield from filters_panel(
        filters,
        "html-slides",
        "html (web) slides",
        previous_filters,
        panel_title="HTML (web) Slides Filters",
    )


def html_slides_post_actions():
    post_actions = settings["html"]["slides"]["post"]
    html_post_actions = settings["html"]["post"]
    general_post_actions = settings["general"]["post"]
    html_post_actions = [(post_action, "html") for post_action in html_post_actions]
    general_post_actions = [(post_action, "general") for post_action in general_post_actions]
    previous_post_actions = html_post_actions + general_post_actions
    yield from post_actions_panel(
        post_actions,
        "html-slides",
        "html (web) slides",
        previous_post_actions,
        panel_title="HTML (web) Slides post-actions",
    )


def html_slides_preambles():
    preambles = settings["html"]["slides"]["preamble"]
    html_preambles = settings["html"]["preamble"]
    general_preambles = settings["general"]["preamble"]
    html_preambles = [(preamble, "html") for preamble in html_preambles]
    general_preambles = [(preamble, "general") for preamble in general_preambles]
    previous_preambles = html_preambles + general_preambles
    yield from preambles_panel(
        preambles,
        "html-slides",
        "html (web) slides",
        previous_preambles,
        panel_title="HTML (web) Slides Preambles",
    )


# endregion

# endregion


def to_id_format(s: str) -> str:
    return s.replace("/", "-").replace("$", "-").replace(".", "-")


class ConfigurationApp(App):
    """Configuration app for lecturemd"""

    CSS = read_css(["ncl.tcss", "configure.tcss"])

    BINDINGS = [
        ("ctrl+s", "save", "Save Changes"),
        ("ctrl+e", "save_and_exit", "Save and Exit"),
        ("ctrl+d", "discard_and_exit", "Discard and Exit")
    ]

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""
        # Footer to show keys
        with Center():
            yield Footer()

            # Add the TabbedContent widget
            with TabbedContent(initial="general"):
                with TabPane("General", id="general"):
                    with VerticalScroll():
                        yield from general_settings()
                with TabPane("LaTeX (pdf)", id="latex"):
                    with VerticalScroll():
                        yield from latex_settings()
                with TabPane("HTML (web)", id="html"):
                    with VerticalScroll():
                        yield from html_settings()

            with Horizontal(classes="buttons"):
                yield Button(
                    "Discard and Exit", id="discard_and_exit", classes="warning"
                )
                yield Button("Save and Exit", id="save_and_exit", classes="save")

    def on_input_changed(self, message):
        id = message.input.id
        if id in settings_map:
            keys = settings_map[id]
            if isinstance(keys, tuple):
                keys, callback = keys
                value = callback(message.value)
            else:
                value = message.value
            global settings
            set_from_keys_list(settings, keys, value)

    def on_switch_changed(self, message):
        id = message.switch.id
        if id in settings_map:
            keys = settings_map[id]
            if isinstance(keys, tuple):
                keys, callback = keys
                value = callback(message.value)
            else:
                value = message.value
            global settings
            set_from_keys_list(settings, keys, value)

    def on_select_changed(self, message):
        id = message.select.id
        if id in settings_map:
            keys = settings_map[id]
            if isinstance(keys, tuple):
                keys, callback = keys
                value = callback(message.value)
            else:
                value = message.value
            global settings
            set_from_keys_list(settings, keys, value)

    def handle_remove_filter(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_remove_from: List[str] | None = None,
    ):
        filter = id[len(f"remove-{prefix}-filter-") :]
        filters = get_from_keys_list(settings, keys)
        for f in filters:
            if (
                list(f.keys())[0].replace("/", "-").replace("$", "-").replace(".", "-")
                == filter
            ):
                filters.remove(f)
                break
        else:
            raise ValueError(f'Filter "{filter}" not found')
        self.query_one(f"#{prefix}-filter-{filter}").remove()
        if also_remove_from is not None:
            for other_prefix in also_remove_from:
                self.query_one(f"#{other_prefix}-filter-{filter}").remove()

    def handle_add_filter(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_add_to: List[str] | None = None,
    ):
        filter = self.query_one(f"#{prefix}-filters-add").value
        order = int(self.query_one(f"#{prefix}-filters-add-order").value)
        filters = get_from_keys_list(settings, keys)
        filters.append({filter: order})
        self.query_one(f"#{prefix}-filters-add").value = ""
        self.query_one(f"#{prefix}-filters-add-order").value = "0"
        new_filter_label = Label(filter, classes="file")
        new_filter_order = Label(str(order), classes="order")
        new_filter_remove = Button(
            "\U0001F5D1",
            id=f"remove-{prefix}-filter-{to_id_format(filter)}",
            classes="remove",
        )
        new_filter_row = Horizontal(
            new_filter_label,
            new_filter_order,
            new_filter_remove,
            id=f"{prefix}-filter-{to_id_format(filter)}",
            classes="row",
        )
        try:
            self.query_one(f"#{prefix}-filters-none").remove()
        except:
            pass
        self.query_one(f"#{prefix}-filters-grid").mount(new_filter_row)
        if also_add_to is not None:
            for other_prefix in also_add_to:
                new_filter_label = Label(filter, classes="file")
                new_filter_order = Label(str(order), classes="order")
                new_filter_source = Label(f"(from {prefix})", classes="source")
                new_filter_row = Horizontal(
                    new_filter_label,
                    new_filter_order,
                    new_filter_source,
                    id=f"{other_prefix}-filter-{to_id_format(filter)}",
                    classes="row",
                )
                try:
                    self.query_one(f"#{other_prefix}-filters-none").remove()
                except:
                    pass
                self.query_one(f"#{other_prefix}-filters-grid").mount(new_filter_row)

    def handle_remove_post_action(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_remove_from: List[str] | None = None,
    ):
        post_action = id[len(f"remove-{prefix}-post-action-") :]
        post_actions = get_from_keys_list(settings, keys)
        for f in post_actions:
            if (
                list(f.keys())[0].replace("/", "-").replace("$", "-").replace(".", "-")
                == post_action
            ):
                post_actions.remove(f)
                break
        else:
            raise ValueError(f'Post-action "{post_action}" not found')
        self.query_one(f"#{prefix}-post-action-{post_action}").remove()
        if also_remove_from is not None:
            for other_prefix in also_remove_from:
                self.query_one(f"#{other_prefix}-post-action-{post_action}").remove()

    def handle_add_post_action(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_add_to: List[str] | None = None,
    ):
        post_action = self.query_one(f"#{prefix}-post-actions-add").value
        order = int(self.query_one(f"#{prefix}-post-actions-add-order").value)
        post_actions = get_from_keys_list(settings, keys)
        post_actions.append({post_action: order})
        self.query_one(f"#{prefix}-post-actions-add").value = ""
        self.query_one(f"#{prefix}-post-actions-add-order").value = "0"
        new_post_action_label = Label(post_action, classes="file")
        new_post_action_order = Label(str(order), classes="order")
        new_post_action_remove = Button(
            "\U0001F5D1",
            id=f"remove-{prefix}-post-action-{to_id_format(post_action)}",
            classes="remove",
        )
        new_post_action_row = Horizontal(
            new_post_action_label,
            new_post_action_order,
            new_post_action_remove,
            id=f"{prefix}-post-action-{to_id_format(post_action)}",
            classes="row",
        )
        try:
            self.query_one(f"#{prefix}-post-actions-none").remove()
        except:
            pass
        self.query_one(f"#{prefix}-post-actions-grid").mount(new_post_action_row)
        if also_add_to is not None:
            for other_prefix in also_add_to:
                new_post_action_label = Label(post_action, classes="file")
                new_post_action_order = Label(str(order), classes="order")
                new_post_action_source = Label(f"(from {prefix})", classes="source")
                new_post_action_row = Horizontal(
                    new_post_action_label,
                    new_post_action_order,
                    new_post_action_source,
                    id=f"{other_prefix}-post-action-{to_id_format(post_action)}",
                    classes="row",
                )
                try:
                    self.query_one(f"#{other_prefix}-post-actions-none").remove()
                except:
                    pass
                self.query_one(f"#{other_prefix}-post-actions-grid").mount(new_post_action_row)

    def handle_remove_preamble(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_remove_from: List[str] | None = None,
    ):
        preamble = id[len(f"remove-{prefix}-preamble-") :]
        preambles = get_from_keys_list(settings, keys)
        for p in preambles:
            if to_id_format(p) == preamble:
                preambles.remove(p)
                break
        else:
            raise ValueError(f'Preamble "{preamble}" not found in {preambles} ({keys})')
        self.query_one(f"#{prefix}-preamble-{preamble}").remove()

        if also_remove_from is not None:
            for other_prefix in also_remove_from:
                self.query_one(f"#{other_prefix}-preamble-{preamble}").remove()

    def handle_add_preamble(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_add_to: List[str] | None = None,
    ):
        preamble = self.query_one(f"#{prefix}-preambles-add").value
        get_from_keys_list(settings, keys).append(preamble)
        self.query_one(f"#{prefix}-preambles-add").value = ""
        new_preamble_label = Label(preamble, classes="file")
        new_preamble_remove = Button(
            "\U0001F5D1",
            id=f"remove-{prefix}-preamble-{to_id_format(preamble)}",
            classes="remove",
        )
        new_preamble_row = Horizontal(
            new_preamble_label,
            new_preamble_remove,
            id=f"{prefix}-preamble-{to_id_format(preamble)}",
            classes="row",
        )
        try:
            self.query_one(f"#{prefix}-preambles-none").remove()
        except:
            pass
        self.query_one(f"#{prefix}-preambles-grid").mount(new_preamble_row)
        if also_add_to is not None:
            for other_prefix in also_add_to:
                new_preamble_label = Label(preamble, classes="file")
                new_preamble_source = Label(f"(from {prefix})", classes="source")
                new_preamble_row = Horizontal(
                    new_preamble_label,
                    new_preamble_source,
                    id=f"{other_prefix}-preamble-{to_id_format(preamble)}",
                    classes="row",
                )
                try:
                    self.query_one(f"#{other_prefix}-preambles-none").remove()
                except:
                    pass
                self.query_one(f"#{other_prefix}-preambles-grid").mount(
                    new_preamble_row
                )

    def handle_remove_style(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_remove_from: List[str] | None = None,
    ):
        style = id[len(f"remove-{prefix}-style-") :]
        styles = get_from_keys_list(settings, keys)
        for s in styles:
            if to_id_format(s) == style:
                styles.remove(s)
                break
        else:
            raise ValueError(f'Style "{style}" not found in {styles} ({keys})')
        self.query_one(f"#{prefix}-style-{style}").remove()

        if also_remove_from is not None:
            for other_prefix in also_remove_from:
                self.query_one(f"#{other_prefix}-style-{style}").remove()

    def handle_add_style(
        self,
        id: str,
        prefix: str,
        keys: List[str],
        also_add_to: List[str] | None = None,
    ):
        style = self.query_one(f"#{prefix}-styles-add").value
        get_from_keys_list(settings, keys).append(style)
        self.query_one(f"#{prefix}-styles-add").value = ""
        new_style_label = Label(style, classes="file")
        new_style_remove = Button(
            "\U0001F5D1",
            id=f"remove-{prefix}-style-{to_id_format(style)}",
            classes="remove",
        )
        new_style_row = Horizontal(
            new_style_label,
            new_style_remove,
            id=f"{prefix}-style-{to_id_format(style)}",
            classes="row",
        )
        try:
            self.query_one(f"#{prefix}-styles-none").remove()
        except:
            pass
        self.query_one(f"#{prefix}-styles-grid").mount(new_style_row)
        if also_add_to is not None:
            for other_prefix in also_add_to:
                new_style_label = Label(style, classes="file")
                new_style_source = Label(f"(from {prefix})", classes="source")
                new_style_row = Horizontal(
                    new_style_label,
                    new_style_source,
                    id=f"{other_prefix}-style-{to_id_format(style)}",
                    classes="row",
                )
                try:
                    self.query_one(f"#{other_prefix}-styles-none").remove()
                except:
                    pass
                self.query_one(f"#{other_prefix}-styles-grid").mount(new_style_row)

    def on_button_pressed(self, message):
        global settings
        id = message.button.id

        if id.endswith("-filters-help"):
            self.push_screen(FiltersDescriptionScreen())
            return

        if id.endswith("-post-actions-help"):
            self.push_screen(PostActionsDescriptionScreen())
            return

        if id.startswith("remove-general-filter"):
            self.handle_remove_filter(
                id,
                "general",
                ["general", "filters"],
                also_remove_from=["latex", "latex-notes", "latex-slides"],
            )
            return

        if id == "general-filters-add-button":
            self.handle_add_filter(
                id,
                "general",
                ["general", "filters"],
                also_add_to=["latex", "latex-notes", "latex-slides"],
            )
            return

        if id.startswith("remove-general-preamble"):
            self.handle_remove_preamble(
                id,
                "general",
                ["general", "preamble"],
                also_remove_from=["latex", "latex-notes", "latex-slides"],
            )
            return

        if id == "general-preambles-add-button":
            self.handle_add_preamble(
                id,
                "general",
                ["general", "preamble"],
                also_add_to=["latex", "latex-notes", "latex-slides"],
            )
            return

        if id.startswith("remove-general-maths-preamble"):
            self.handle_remove_preamble(
                id,
                "general-maths",
                ["general", "maths preamble"],
                also_remove_from=[
                    "general",
                    "latex",
                    "latex-notes",
                    "latex-slides",
                    "html",
                    "html-notes",
                    "html-slides",
                ],
            )
            return

        if id == "general-maths-preambles-add-button":
            self.handle_add_preamble(
                id,
                "general-maths",
                ["general", "maths preamble"],
                also_add_to=[
                    "general",
                    "latex",
                    "latex-notes",
                    "latex-slides",
                    "html",
                    "html-notes",
                    "html-slides",
                ],
            )
            return

        if id.startswith("remove-latex-filter"):
            self.handle_remove_filter(
                id,
                "latex",
                ["latex", "filters"],
                also_remove_from=["latex-notes", "latex-slides"],
            )
            return

        if id == "latex-filters-add-button":
            self.handle_add_filter(
                id,
                "latex",
                ["latex", "filters"],
                also_add_to=["latex-notes", "latex-slides"],
            )
            return

        if id.startswith("remove-latex-preamble"):
            self.handle_remove_preamble(
                id,
                "latex",
                ["latex", "preamble"],
                also_remove_from=["latex-notes", "latex-slides"],
            )
            return

        if id == "latex-preambles-add-button":
            self.handle_add_preamble(
                id,
                "latex",
                ["latex", "preamble"],
                also_add_to=["latex-notes", "latex-slides"],
            )
            return

        if id.startswith("remove-latex-notes-filter"):
            self.handle_remove_filter(id, "latex-notes", ["latex", "notes", "filters"])
            return

        if id == "latex-notes-filters-add-button":
            self.handle_add_filter(id, "latex-notes", ["latex", "notes", "filters"])
            return

        if id.startswith("remove-latex-notes-preamble"):
            self.handle_remove_preamble(
                id, "latex-notes", ["latex", "notes", "preamble"]
            )
            return

        if id == "latex-notes-preambles-add-button":
            self.handle_add_preamble(id, "latex-notes", ["latex", "notes", "preamble"])
            return

        if id.startswith("remove-latex-slides-filter"):
            self.handle_remove_filter(
                id, "latex-slides", ["latex", "slides", "filters"]
            )
            return

        if id == "latex-slides-filters-add-button":
            self.handle_add_filter(id, "latex-slides", ["latex", "slides", "filters"])
            return

        if id.startswith("remove-latex-slides-preamble"):
            self.handle_remove_preamble(
                id, "latex-slides", ["latex", "slides", "preamble"]
            )
            return

        if id == "latex-slides-preambles-add-button":
            self.handle_add_preamble(
                id, "latex-slides", ["latex", "slides", "preamble"]
            )
            return

        if id.startswith("remove-html-style"):
            self.handle_remove_style(
                id,
                "html",
                ["html", "styles"],
                also_remove_from=["html-notes", "html-slides"],
            )
            return

        if id == "html-styles-add-button":
            self.handle_add_style(
                id,
                "html",
                ["html", "styles"],
                also_add_to=["html-notes", "html-slides"],
            )
            return

        if id.startswith("remove-html-filter"):
            self.handle_remove_filter(
                id,
                "html",
                ["html", "filters"],
                also_remove_from=["html-notes", "html-slides"],
            )
            return

        if id == "html-filters-add-button":
            self.handle_add_filter(
                id,
                "html",
                ["html", "filters"],
                also_add_to=["html-notes", "html-slides"],
            )
            return

        if id.startswith("remove-html-preamble"):
            self.handle_remove_preamble(
                id,
                "html",
                ["html", "preamble"],
                also_remove_from=["html-notes", "html-slides"],
            )
            return

        if id == "html-preambles-add-button":
            self.handle_add_preamble(
                id,
                "html",
                ["html", "preamble"],
                also_add_to=["html-notes", "html-slides"],
            )
            return

        if id.startswith("remove-html-notes-style"):
            self.handle_remove_style(id, "html-notes", ["html", "notes", "styles"])
            return

        if id == "html-notes-styles-add-button":
            self.handle_add_style(id, "html-notes", ["html", "notes", "styles"])
            return

        if id.startswith("remove-html-notes-filter"):
            self.handle_remove_filter(id, "html-notes", ["html", "notes", "filters"])
            return

        if id == "html-notes-filters-add-button":
            self.handle_add_filter(id, "html-notes", ["html", "notes", "filters"])
            return

        if id.startswith("remove-html-notes-preamble"):
            self.handle_remove_preamble(id, "html-notes", ["html", "notes", "preamble"])
            return

        if id == "html-notes-preambles-add-button":
            self.handle_add_preamble(id, "html-notes", ["html", "notes", "preamble"])
            return

        if id.startswith("remove-html-slides-style"):
            self.handle_remove_style(id, "html-slides", ["html", "slides", "styles"])
            return

        if id == "html-slides-styles-add-button":
            self.handle_add_style(id, "html-slides", ["html", "slides", "styles"])
            return

        if id.startswith("remove-html-slides-filter"):
            self.handle_remove_filter(id, "html-slides", ["html", "slides", "filters"])
            return

        if id == "html-slides-filters-add-button":
            self.handle_add_filter(id, "html-slides", ["html", "slides", "filters"])
            return

        if id.startswith("remove-html-slides-preamble"):
            self.handle_remove_preamble(
                id, "html-slides", ["html", "slides", "preamble"]
            )
            return

        if id == "html-slides-preambles-add-button":
            self.handle_add_preamble(id, "html-slides", ["html", "slides", "preamble"])
            return

    def action_save(self):
        write_settings(base_dir, settings)
        self.notify("Changes have been saved", title = "Saved", severity="information", timeout = 2)

    def action_save_and_exit(self):
        self.exit()

    def action_discard_and_exit(self):
        self.discard_and_exit_pressed("")

    @on(Button.Pressed, "#save_and_exit")
    def save_and_exit(self, message):
        self.exit()

    @on(Button.Pressed, "#discard_and_exit")
    def discard_and_exit_pressed(self, message):
        self.push_screen(ConfirmationScreen(), self.maybe_discard_and_exit)

    def maybe_discard_and_exit(self, response: str):
        global settings
        if response == "modal_yes":
            del settings
            settings = deepcopy(original_settings)
            self.exit()


def main():
    global settings, original_settings, base_dir
    base_dir = Path(".").resolve()
    settings = read_settings(base_dir)
    original_settings = deepcopy(settings)
    app = ConfigurationApp()
    app.run()
    write_settings(base_dir, settings)


if __name__ == "__main__":
    main()
