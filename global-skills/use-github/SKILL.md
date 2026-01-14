---
name: use-github
description: Skill para interactuar con GitHub API - gestionar repositorios, issues y pull requests
---

# GitHub API Skill

Skill para interactuar con la API de GitHub mediante scripts CLI de Python.

## Cuando usar este skill

Usa este skill cuando necesites:

- Listar repositorios de un usuario
- Obtener informacion de un repositorio
- Gestionar issues (listar, crear, actualizar)
- Gestionar pull requests (listar, crear, mergear)
- Listar branches de un repositorio
- Obtener contenido de archivos
- Buscar en el codigo

## Requisitos

- Variable de entorno `GITHUB_TOKEN` configurada con un token de acceso personal
- Python 3.11+ instalado
- Dependencias instaladas: `pip install -r requirements.txt`

## Comandos disponibles

### Listar repositorios

```bash
python scripts/list_repos.py
python scripts/list_repos.py --user octocat
python scripts/list_repos.py --type owner
```

### Obtener info de repositorio

```bash
python scripts/get_repo.py --repo owner/repo-name
```

### Listar issues

```bash
python scripts/list_issues.py --repo owner/repo-name
python scripts/list_issues.py --repo owner/repo-name --state open
python scripts/list_issues.py --repo owner/repo-name --state closed --labels bug,enhancement
```

### Crear issue

```bash
python scripts/create_issue.py --repo owner/repo-name --title "Bug encontrado" --body "Descripcion del bug"
python scripts/create_issue.py --repo owner/repo-name --title "Nueva feature" --labels enhancement --assignees user1,user2
```

### Actualizar issue

```bash
python scripts/update_issue.py --repo owner/repo-name --issue-number 123 --state closed
python scripts/update_issue.py --repo owner/repo-name --issue-number 123 --title "Nuevo titulo" --labels bug,urgent
```

### Listar pull requests

```bash
python scripts/list_prs.py --repo owner/repo-name
python scripts/list_prs.py --repo owner/repo-name --state open
python scripts/list_prs.py --repo owner/repo-name --state all
```

### Crear pull request

```bash
python scripts/create_pr.py --repo owner/repo-name --title "Mi PR" --head feature-branch --base main
python scripts/create_pr.py --repo owner/repo-name --title "Mi PR" --body "Descripcion de cambios" --head feature-branch --base main
```

### Mergear pull request

```bash
python scripts/merge_pr.py --repo owner/repo-name --pr-number 42
python scripts/merge_pr.py --repo owner/repo-name --pr-number 42 --merge-method squash
python scripts/merge_pr.py --repo owner/repo-name --pr-number 42 --merge-method rebase
```

### Listar branches

```bash
python scripts/list_branches.py --repo owner/repo-name
```

### Obtener archivo

```bash
python scripts/get_file.py --repo owner/repo-name --path README.md
python scripts/get_file.py --repo owner/repo-name --path src/main.py --ref develop
```

### Buscar en codigo

```bash
python scripts/search_code.py --query "def main"
python scripts/search_code.py --query "class User" --repo owner/repo-name
```

## Formato de salida

Todos los comandos devuelven JSON valido:

- Exito: JSON con los datos solicitados
- Error: `{"error": "mensaje de error"}`

## Ejemplos de uso comun

### Revisar issues abiertos y comentar

```bash
# Listar issues abiertos
python scripts/list_issues.py --repo owner/repo --state open

# Ver detalles de un repo
python scripts/get_repo.py --repo owner/repo
```

### Flujo de PR

```bash
# Crear PR
python scripts/create_pr.py --repo owner/repo --title "Fix bug" --head fix-branch --base main

# Listar PRs abiertos
python scripts/list_prs.py --repo owner/repo --state open

# Mergear PR
python scripts/merge_pr.py --repo owner/repo --pr-number 42 --merge-method squash
```
