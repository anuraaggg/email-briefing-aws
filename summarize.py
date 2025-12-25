KEYWORDS = [
    "action", "deadline", "meeting", "review",
    "approve", "approval", "follow up", "confirm"
]

def summarize(emails):
    action = []
    fyi = []

    for sender, subject in emails:
        subject_lower = subject.lower()

        item = f"{sender} – {subject}"

        if any(k in subject_lower for k in KEYWORDS):
            action.append(item)
        else:
            fyi.append(item)

    action = list(dict.fromkeys(action))
    fyi = list(dict.fromkeys(fyi))

    lines = []

    lines.append(f"Needs Action ({len(action)})")
    if action:
        for s in action[:5]:
            lines.append(f"- {s}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append(f"FYI ({len(fyi)})")
    for s in fyi[:5]:
        lines.append(f"- {s}")

    return "\n".join(lines)
