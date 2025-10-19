import argparse
from models import User
from auth import AuthUser

parser = argparse.ArgumentParser(description='Secure Login System')
sub_parser = parser.add_subparsers(dest='command')
add_user = sub_parser.add_parser('add',help='to add a user to the database')
add_user.add_argument('--p',required=True,help='Database address')
add_user.add_argument('name',help='name for user')
add_user.add_argument('lastname',help='lastname for user')
add_user.add_argument('phone',help='phone for user')
add_user.add_argument('password',help='password for user (at least 8 digits for greater security)')
add_user.add_argument('--email',required=True,help='email for user')

delete_user = sub_parser.add_parser("del",help="To delete a user from database")
delete_user.add_argument("--p",required=True,help="Database path")
delete_user.add_argument("--phone",required=True,help="User mobile number to delete")

args = parser.parse_args()

if args.command == 'add' :
    pd = AuthUser(path_db=args.p)
    user = User(name=args.name,lastname=args.lastname,phone=args.phone,password=args.password,email=args.email)
    pd.Add_User(user)
if args.command == "del"
    path_db = AuthUser(path_db=args.p)
    path_db.Delete_User(phone=args.phone)

