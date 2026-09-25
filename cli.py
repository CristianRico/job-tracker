# python -m job_tracker add --company "Acme" --position "Junior Python Dev" [--url ...] [--notes ...]
# python -m job_tracker list [--status applied]
# python -m job_tracker show ID
# python -m job_tracker update ID --status interview
# python -m job_tracker delete ID
# python -m job_tracker stats          # nº de candidaturas por estado

import argparse
import repository as db

def build_parser():
    parser = argparse.ArgumentParser(prog='Job Tracker', 
                                     usage='%(prog)s [options]',
                                     description="Job Tracker CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Añadir candidatura")
    p_add.add_argument("--company", required=True)
    p_add.add_argument("--position", required=True)
    p_add.add_argument("--url")
    p_add.add_argument("--notes")

    p_list = sub.add_parser("list", help="Lista de candidaturas")
    p_list.add_argument("--status", help="Filtra por Estado", choices=db.VALID_STATUSES)

    p_show = sub.add_parser("show", help="Muestra una candidatura por ID")
    p_show.add_argument("id", type=int)

    p_update = sub.add_parser("update", help="Actualiza el estado de una candidatura con [id].")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--status", required=True)

    p_delete = sub.add_parser("delete", help="Elimina una candidatura con [id].")
    p_delete.add_argument("id", type=int)

    sub.add_parser("stats", help="Muestra el número de candidaturas por estado")

    return parser

if __name__ == "__main__":
    args = build_parser().parse_args()

    if args.command == "add":
        print("Add")
    elif args.command == "list":
        pass
    elif args.command == "show":
        pass
    elif args.command == "update":
        pass
    elif args.command == "delete":
        pass
    elif args.command == "stats":
        pass


