#!/bin/bash
# Clear and rebuild the Skill table from the enum.
# Run from project root: ./scripts/rebuild_skills.sh

cd "$(dirname "$0")/.." || exit 1

python manage.py shell -c "
from skills.models import Skill
from enums.skills import Skills

Skill.objects.all().delete()
for skill in Skills:
    Skill.objects.get_or_create(name=skill.value)

print(f'Synced {Skill.objects.count()} skills from enum.')
"
