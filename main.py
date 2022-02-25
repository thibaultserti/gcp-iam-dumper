#!/usr/bin/env python3

# Script to dump GCP IAM

import argparse
import csv
from itertools import zip_longest
import logging
from re import M
import sys

from functions import retrieve_iam_json
from models import Member, Role

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", type=str, help="project to retrieve IAM from", required=True)
parser.add_argument("-o", "--output", type=str, default="", help="output", required=False)
parser.add_argument("--only-user", action="store_true", help="retrieve only users, not groups, not SA", required=False)
parser.add_argument("--only-physical", action="store_true", help="retrieve only users and groups, not SA", required=False)
parser.add_argument("-s", "--short", action="store_true", help="use short", required=False)
args = parser.parse_args()

if args.output == "":
    args.output = args.project 

if args.only_physical and args.only_user:
    logging.critical("Do not user --only-user and --only-physical at the same time")
    sys.exit(1)

ROLES = {}
MEMBERS = {}

list_iam = retrieve_iam_json(args.project)

for dico in list_iam:
    if args.short:
        role = dico["role"].split("/")[1]
    else:
        role = dico["role"]

    members = dico["members"]
    # Create or fill roles object
    if role not in ROLES:
        ROLES[role] = Role(name=role)
    for member in members:
        if args.short:
            ROLES[role].add_member(member.split(":")[1])
        else:
            ROLES[role].add_member(member)
            
    # Create or fill roles member
    for member in members:
        if member not in MEMBERS:
            if args.short:
                MEMBERS[member] = Member(name=member.split(":")[1])
            else:
                MEMBERS[member] = Member(name=member)
        MEMBERS[member].add_role(role)

# only keep required
if args.only_user:
    MEMBERS_FILTERED = {m_id: m for m_id,m in MEMBERS.items() if MEMBERS[m_id].is_user()}
    for r_id,r in ROLES.items():
        m_filtered = [m for m in r.members if MEMBERS[m].is_user()]
        r.members = m_filtered
    ROLES_FILTERED = {r_id: r for r_id,r in ROLES.items() if ROLES[r_id].members != []}

elif args.only_physical:
    MEMBERS_FILTERED = {m_id: m for m_id,m in MEMBERS if MEMBERS[m_id].is_physical()}
    for r_id,r in ROLES.items():
        m_filtered = [m for m in r.members if MEMBERS[m].is_physical()]
        r.members = m_filtered
    ROLES_FILTERED = {r_id: r for r_id,r in ROLES.items() if ROLES[r_id].members != []}

else:
    MEMBERS_FILTERED = MEMBERS
    ROLES_FILTERED = ROLES

members = {m_id: list(m.roles) for m_id, m in MEMBERS_FILTERED.items()}
roles = {r_id: list(r.members) for r_id, r in ROLES_FILTERED.items()}


with open(args.output+"_members.csv", 'w', newline='') as csvfile:
    fieldnames = MEMBERS_FILTERED.keys()
    writer = csv.writer(csvfile)
    writer.writerow(members.keys())
    writer.writerows(list(zip_longest(*members.values(), fillvalue='')))

with open(args.output+"_roles.csv", 'w', newline='') as csvfile:
    fieldnames = ROLES_FILTERED.keys()
    writer = csv.writer(csvfile)
    writer.writerow(roles.keys())
    writer.writerows(list(zip_longest(*roles.values(), fillvalue='')))
