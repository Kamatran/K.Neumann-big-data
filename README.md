# Big Data — projekt

*English version below.*

Repozytorium Twojego projektu na cały semestr. Rozwijasz je tydzień po tygodniu, a stan
repozytorium jest oceniany w czterech punktach kontrolnych.

## Jak powstało to repozytorium

Przyciskiem **„Use this template"**, nie przez fork. Repozytorium jest Twoje: niezależne
od repozytorium prowadzącego i nie zniknie, gdy po semestrze skończy się Twój dostęp do
materiałów kursu.

**Dodaj prowadzącego jako współpracownika:** *Settings → Collaborators → Add people* →
`kubiak-mateusz`. Bez tego nie zobaczę Twojej pracy.

## Struktura

| Katalog | Co tu trafia |
|---|---|
| katalog główny | pliki Compose i `Dockerfile` |
| `src/` | kod w Pythonie |
| `scripts/` | skrypty uruchomieniowe |
| `data/` | dane — **nie trafiają do Gita** (`.gitignore`) |
| `out/` | wyniki zadań, które oddajesz — **trafiają do Gita** |

Co gdzie skopiować z repozytorium materiałów, mówi `README.md` w katalogu danego tygodnia.
Pliki kopiujesz ręcznie — **nigdy `git pull` z repozytorium materiałów do tego**.

## Rytm pracy

Gałąź na tydzień (`week-01`, `week-02`, …) → commity → push → merge request → merge.
Push **najpóźniej przed kolejnymi zajęciami**.

Punkt kontrolny oznaczasz tagiem, na zajęciach, razem z prowadzącym — pierwszy to
`v0.4-hadoop-done` po czterech tygodniach.

## Notatki

Możesz prowadzić notatki w plikach Markdown w tym repozytorium — to dobre miejsce, bo są
obok kodu, którego dotyczą. **Nie jest to wymagane** i równie dobrze możesz notować
w dowolnym innym narzędziu. Zrozumienie własnego rozwiązania sprawdzam w rozmowie.

---

# Big Data — project

The repository for your project for the whole semester. You develop it week by week, and its
state is assessed at four checkpoints.

## How this repository was created

With the **"Use this template"** button, not as a fork. The repository is yours: independent of
the lecturer's repository, and it will not disappear when your access to the course materials
ends after the semester.

**Add the lecturer as a collaborator:** *Settings → Collaborators → Add people* →
`kubiak-mateusz`. Without this I cannot see your work.

## Structure

| Directory | What goes here |
|---|---|
| root | Compose files and `Dockerfile` |
| `src/` | Python code |
| `scripts/` | run scripts |
| `data/` | data — **never committed** (`.gitignore`) |
| `out/` | task results you hand in — **committed** |

The `README.md` in each week's directory of the materials repository says which file goes where.
Copy files by hand — **never `git pull` from the materials repository into this one**.

## Working rhythm

One branch per week (`week-01`, `week-02`, …) → commits → push → merge request → merge.
Push **before the next class at the latest**.

You mark a checkpoint with a tag, in class, together with the lecturer — the first one is
`v0.4-hadoop-done` after four weeks.

## Notes

You may keep notes in Markdown files in this repository — it is a good place, next to the code
they refer to. **It is not required**, and you can just as well use any other tool. I check your
understanding of your own solution in conversation.
