from __future__ import annotations

import json
import os
from pathlib import Path

CODEQL_LANGUAGE_BY_FILE = {
    ".c": "c-cpp", ".cc": "c-cpp", ".cpp": "c-cpp", ".h": "c-cpp", ".hpp": "c-cpp",
    ".cs": "csharp", ".go": "go", ".java": "java-kotlin", ".kt": "java-kotlin",
    ".kts": "java-kotlin", ".js": "javascript-typescript", ".jsx": "javascript-typescript",
    ".ts": "javascript-typescript", ".tsx": "javascript-typescript", ".py": "python",
    ".rb": "ruby", ".rs": "rust", ".swift": "swift",
}

DISPLAY = {
    "c-cpp": "C/C++", "csharp": "C#", "go": "Go", "java-kotlin": "Java/Kotlin",
    "javascript-typescript": "JavaScript/TypeScript", "python": "Python", "ruby": "Ruby",
    "rust": "Rust", "swift": "Swift",
}

MANIFESTS = {
    "requirements.txt": "Python requirements",
    "pyproject.toml": "Python project",
    "package.json": "npm package",
    "package-lock.json": "npm lockfile",
    "go.mod": "Go modules",
    "Cargo.toml": "Cargo",
    "pom.xml": "Maven",
    "build.gradle": "Gradle",
    "build.gradle.kts": "Gradle Kotlin DSL",
    "Gemfile": "Bundler",
}


def profile(root: Path) -> dict[str, object]:
    languages: set[str] = set()
    ignored = {".git", ".venv", "node_modules", "dist", "build", "coverage"}

    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        language = CODEQL_LANGUAGE_BY_FILE.get(path.suffix.lower())
        if language:
            languages.add(language)

    manifests = [label for name, label in MANIFESTS.items() if (root / name).exists()]
    if (root / "go.mod").exists():
        languages.add("go")
    if (root / "pom.xml").exists() or (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        languages.add("java-kotlin")
    if (root / "Gemfile").exists():
        languages.add("ruby")
    if (root / "Cargo.toml").exists():
        languages.add("rust")

    unsupported_code = sorted({
        path.suffix.lower()
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".php", ".scala"}
        and not any(part in ignored for part in path.parts)
    })

    return {
        "codeql_languages": sorted(languages),
        "languages": [DISPLAY[x] for x in sorted(languages)],
        "manifests": manifests,
        "unsupported_extensions": unsupported_code,
    }


def main() -> None:
    data = profile(Path.cwd())
    print(json.dumps(data, indent=2))
    codeql = ",".join(data["codeql_languages"])
    unsupported = ",".join(data["unsupported_extensions"])
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"codeql_languages={codeql}\n")
            handle.write(f"unsupported_extensions={unsupported}\n")
    print(f"::notice::Detected CodeQL languages: {codeql or 'none'}")
    if data["unsupported_extensions"]:
        print(f"::warning::Unsupported-by-CodeQL source extensions detected: {', '.join(data['unsupported_extensions'])}")


if __name__ == "__main__":
    main()
