r"""Convert ../manuscript_draft.md into LaTeX pieces for main.tex.

- '# Abstract'                     -> sections/abstract.tex (bold run-in labels kept)
- '# 1. Introduction' ... '# 6. ...' -> sections/body.tex (manual numbering stripped; LaTeX numbers itself)
- '# Appendix A. ...'              -> sections/appendix.tex
- '[TBD: ...]'                     -> \todo{...} (red), so every gap is visible in the PDF
Markdown stays the source of truth: edit the draft, then run
    python3 prepare.py && tectonic -X compile main.tex
"""
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
DRAFT = HERE.parent / "manuscript_draft.md"


def pandoc(md):
    # '**Table 1. Caption.**' above a pipe table -> a real caption, so LaTeX numbers it and keeps it with the table
    md = re.sub(r"\*\*Table (S?\d+)\.\s*(.+?)\*\*\n\n((?:\|.*\n)+)", lambda m: m.group(3) + "\nTable: " + ("" if m.group(1).isdigit() else f"(Table {m.group(1)}) ") + m.group(2) + "\n", md)
    md = re.sub(r"(?m)^(?!\s*$)(?![-*] |\d+\. |\|)(.+)\n(?=[-*] |\d+\. )", r"\1\n\n", md)  # blank line before lists
    tex = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--wrap=preserve", "--natbib", "--listings", "--columns=100"],
                         input=md, capture_output=True, text=True, check=True).stdout
    tex = re.sub(r"\{\[\}TBD:?\s*(.*?)\{\]\}", r"\\todo{\1}", tex, flags=re.S)
    tex = tex.replace(r"{[}TBD{]}", r"\todo{}")
    return tex


def main():
    md = DRAFT.read_text(encoding="utf-8")
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)           # YAML front matter
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)                    # author notes
    parts = re.split(r"(?m)^# ", md)
    chunks = {p.split("\n", 1)[0].strip(): p.split("\n", 1)[1] for p in parts if p.strip()}

    abstract = chunks.pop("Abstract")
    abstract, _, kw = abstract.partition("**Keywords:**")
    (HERE / "sections/abstract.tex").write_text(pandoc(abstract), encoding="utf-8")
    keywords = r" \sep ".join(k.strip() for k in kw.strip().split(";"))
    (HERE / "sections/keywords.tex").write_text(keywords + "\n", encoding="utf-8")

    chunks.pop("References", None)
    body, appendix = [], []
    for head, text in chunks.items():
        title = re.sub(r"^(\d+\.|Appendix [A-Z]\.)\s*", "", head)
        text = re.sub(r"(?m)^## \d+(\.\d+)*\s+", "## ", text)
        (appendix if head.startswith("Appendix") else body).append(f"# {title}\n{text}")
    (HERE / "sections/body.tex").write_text(pandoc("\n".join(body)), encoding="utf-8")
    (HERE / "sections/appendix.tex").write_text(pandoc("\n".join(appendix)), encoding="utf-8")
    supp = (HERE.parent / "supplementary.md").read_text(encoding="utf-8")
    supp = re.sub(r"(?m)^# (S\d+)\. ", r"# \1. ", supp)
    (HERE / "sections/supp.tex").write_text(re.sub(r"\\caption\{\(Table S\d+\) ", r"\\caption{", pandoc(supp)).replace(r"\section{", r"\section*{"), encoding="utf-8")
    print("wrote sections/{abstract,keywords,body,appendix,supp}.tex")


if __name__ == "__main__":
    main()
