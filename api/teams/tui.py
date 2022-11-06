from ..utils import safe_int_input
from ..users.tui import search_and_select_user

from ..turmas.tui import search_and_select_turma, search_and_select_student

from .common import MEMBERSHIP_CATEGORIES
from .repository import search_members, get_teams, get_teams_from_turma, search_teams, create_team, update_teams, delete_team


def summary_team(team):
    name = team["name"]
    turma_name = team["turma"]["name"]
    members_count = len(team["members"])
    return f"{name} (Turma: {turma_name}, {members_count} membros)"


def summary_member(member):
    name = member["name"]
    email = member["email"]
    category = member["category"]
    category_description = MEMBERSHIP_CATEGORIES[category]

    return f"{name} <{email}> como {category_description}"


def show_members(team, title="Membros:"):
    print(title)
    for member in team["members"]:
        print(f"    - {summary_member(member)}")


def search_and_select_member(team):
    search_term = input("Procurar: ")
    members = search_members(search_term, team)

    if len(members) == 0:
        return None

    for index, member in enumerate(members):
        print(f"{index+1} - {summary_member(member)}")

    while True:
        option = safe_int_input("Opção: ")
        if option > 0 and option <= len(members):
            return members[option - 1]
        print("Opção inválida.")


def select_member(team):
    members = team["members"]

    if len(members) == 0:
        return None

    for index, member in enumerate(members):
        print(f"{index+1} - {summary_member(member)}")

    while True:
        option = safe_int_input("Opção: ")
        if option > 0 and option <= len(members):
            return members[option - 1]
        print("Opção inválida.")


def select_member_or_instructor(team):
    group_leader = team["turma"]["group_leader"]
    fake_client = team["turma"]["fake_client"]
    members = team["members"]

    print(f"1 - {group_leader['name']} como Líder de Grupo")
    print(f"2 - {fake_client['name']} como Fake Client ")

    for index, member in enumerate(members):
        print(f"{index+3} - {summary_member(member)}")

    while True:
        option = safe_int_input("Opção: ")
        if option > 0 and option <= len(members) + 2:
            if option == 1:
                return group_leader
            elif option == 2:
                return fake_client
            else:
                return members[option - 3]
        print("Opção inválida.")


def add_members(team, turma):
    while True:
        should_add = input("Deseja adicionar mais um membro (S/N)? ")
        if should_add == "S" or should_add == "s":
            print("Selecione um Membro")
            new_member = search_and_select_student(turma)
            if new_member is None:
                continue
            new_member["category"] = "COMUM"
            team["members"].append(new_member)
        else:
            break


def remove_members(team):
    while True:
        should_add = input("Deseja remover mais um membro (S/N)? ")
        if should_add == "S" or should_add == "s":
            print("Selecione um Membro")
            member_to_remove = search_and_select_member(team)
            if member_to_remove is None:
                continue
            team["members"].remove(member_to_remove)
        else:
            break


def detail_team(team, title="Detalhes do Time:"):
    id = team["id"]
    name = team["name"]
    turma_name = team["turma"]["name"]

    print(title)
    print(f"Id: {id}")
    print(f"Nome: {name}")
    print(f"Turma:  {turma_name}")
    print("Membros:")

    for member in team["members"]:
        print(f"    - {summary_member(member)}")


def list_teams():
    print("Times:")
    for team in get_teams():
        print(summary_team(team))


def list_members():
    team = search_and_select_team()
    show_members(team)


def search_and_select_team():
    search_term = input("Procurar: ")
    teams = search_teams(search_term)

    if len(teams) == 0:
        return None

    for index, team in enumerate(teams):
        print(f"{index+1} - {summary_team(team)}")

    while True:
        option = safe_int_input("Opção: ")
        if option > 0 and option <= len(teams):
            return teams[option - 1]
        print("Opção inválida.")


def select_team_from_turma(turma):
    teams = get_teams_from_turma(turma)

    if len(teams) == 0:
        print("Nenhuma time encontrado.")
        return None

    for index, team in enumerate(teams):
        print(f"{index+1} - {summary_team(team)}")

    while True:
        option = safe_int_input("Opção: ")
        if option > 0 and option <= len(teams):
            return teams[option - 1]
        print("Opção inválida.")


def show_team():
    team = search_and_select_team()
    if team is None:
        print("Nenhum time encontrado.")
        return
    detail_team(team)


def new_team():
    print("Novo Time")

    print("Selecione a turma:")
    turma = search_and_select_turma()

    if turma is None:
        return

    name = input("Nome: ")

    print("Selecione um Líder Técnico")
    tech_leader = search_and_select_student(turma)
    tech_leader["category"] = "LIDER"

    print("Selecione um Product Owner")
    product_owner = search_and_select_student(turma)
    product_owner["category"] = "PRODU"

    members = [tech_leader, product_owner]

    team = create_team(name, turma, members)
    add_members(team, turma)
    update_teams()


def edit_team():
    print("Editar time")
    team = search_and_select_team()

    if team is None:
        print("Nenhum time encontrado.")
        return

    name = team['name']
    print(f"Nome: {name}")
    should_update = input("Deseja alterar (S/N)? ")
    if should_update == "S" or should_update == "s":
        team["name"] = input("Novo nome: ")

    show_members(team)
    add_members(team, team["turma"])

    show_members(team)
    remove_members(team)

    update_teams()


def remove_team():
    print("Remover time")
    team = search_and_select_team()
    if team is None:
        print("Nenhum time encontrado.")
        return
    delete_team(team)


def admin_teams_menu():
    while True:
        print("Menu Times (Administrador)")
        print("1 - Listar")
        print("2 - Novo")
        print("3 - Buscar e Detalhar")
        print("4 - Editar")
        print("5 - Excluir")
        print("6 - Voltar")

        while True:
            option = safe_int_input("Opção: ")
            if option >= 1 and option <= 6:
                break
            print("Opção inválida.")

        if option == 1:
            list_teams()
        elif option == 2:
            new_team()
        elif option == 3:
            show_team()
        elif option == 4:
            edit_team()
        elif option == 5:
            remove_team()
        else:
            return