# python -m job_tracker add --company "Acme" --position "Junior Python Dev" [--url ...] [--notes ...]
# python -m job_tracker list [--status applied]
# python -m job_tracker show ID
# python -m job_tracker update ID --status interview
# python -m job_tracker delete ID
# python -m job_tracker stats          # nº de candidaturas por estado

import sys
import argparse
from tabulate import tabulate
from job_tracker import repository as db

############
#   UTIL   #
############

def print_job(job):
    data = [[key, job[key]] for key in job.keys()]
    print(tabulate(data, headers=["Campo", "Valor"], tablefmt="simple"))


################
#   DB CALLS   #
################

def _add(conn, args):
    job_id = db.add_job(
                    conn,
                    company=args.company,
                    position=args.position,
                    url=args.url,
                    notes=args.notes
                )
    print(f"Candidatura en {args.company} como {args.position} añadida con id {job_id}")

def _list(conn, args):
    status = args.status.strip() if args.status else None
    jobs = db.list_jobs(conn, status=status)

    if not jobs:
        msg = f"No hay candidaturas con estado '{status}'." if status else "No hay candidaturas todavía."
        print(msg)
    else:
        headers = list(jobs[0].keys())
        print(tabulate(jobs, headers=headers, tablefmt="simple"))

def _show(conn, args):
    job = db.get_job(conn, args.id)
    print_job(job)

def _update(conn, args):
    db.update_job(conn, args.id, args.status)
    job = db.get_job(conn, args.id)
    print_job(job)

def _delete(conn, args):
    db.delete_job(conn, args.id)
    print(f"Se ha eliminado la candidatura {args.id}")

def _stats(conn):
    stat_list = db.count_by_status(conn)
    print(tabulate(stat_list.items(), headers=["Estado", "Total"], tablefmt="simple"))

##############
#   PARSER   #
##############

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


###########
#   CLI   #
###########

if __name__ == "__main__":
    args = build_parser().parse_args()

    conn = db.get_conn()
    db.init_db(conn)
    
    try:
        if args.command == "add":
            _add(conn, args)
        elif args.command == "list":
            _list(conn, args)
        elif args.command == "show":
            _show(conn, args)
        elif args.command == "update":
            _update(conn, args)
        elif args.command == "delete":
            _delete(conn, args)
        elif args.command == "stats":
            _stats(conn, )
    except db.RepoError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
    finally:
        conn.close()