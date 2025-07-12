"""
Utilitários para manipulação e exibição de épicos do sistema.
"""

class Epic:
    """
    Representa um épico do produto, com título e descrição.
    """
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"Epic(title={self.title!r}, description={self.description!r})"

def print_epics(epics):
    """
    Exibe uma lista de épicos formatada no terminal.
    """
    print("\nÉpicos gerados para o produto:\n" + "-"*40)
    for i, epic in enumerate(epics, 1):
        print(f"{i}. {epic.title}")
        print(f"   {epic.description}\n")
    print("-"*40)

def print_user_stories(user_stories):
    """
    Exibe uma história de usuário formatada no terminal.
    """
    for i, user_story in enumerate(user_stories, 1):
        print(f"\nHistória de usuário: {user_story.title}\n" + "-"*40)
        print(f"Descrição: {user_story.description}\n")
        print("-"*40)


