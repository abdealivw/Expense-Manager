from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import User,Expenses,Income

# Create your views here.

# def renderTemplate(req):
#     return render(req,"index.html")

def login(req):
    return render(req,"login.html")

def signup(req):
    return render(req,"sign-up.html")

def savedata(req):
    if req.method=='POST' and req.FILES['upload']:
        upload=req.FILES['upload']
        fss=FileSystemStorage()
        file=fss.save(upload.name,upload)
        obj=User()
        obj.name=req.POST.get('name')
        obj.password=req.POST.get('password')
        obj.email=req.POST.get('email')
        obj.contact=req.POST.get('contact')
        obj.img=file
        obj.save()
        return render(req,"login.html")
    else:
        return HttpResponse("nope")
    

def checklogin(req):
    if req.method=='POST':
        uname=req.POST.get('name')
        upass=req.POST.get('password')
        data=User.objects.filter(name=uname,password=upass)
        if(data):
            listData=data.values()
            req.session['id']=listData[0]['id']
            req.session['name']=listData[0]['name']
            req.session['email']=listData[0]['email']
            req.session['contact']=listData[0]['contact']
            req.session['img']=listData[0]['img']
            return redirect('/dashboardrender')
        else:
            return render(req,"login.html",{'msg':'invalid data'})
    else:
        return render(req,"login.html")
    

def addExpenseRender(req):
    return render(req,"addexpense.html")

def addExpensedata(req):
    if req.method=='POST' and 'id' in req.session:
        obj=Expenses()
        uid=req.session['id']
        obj.date=req.POST.get('date')
        obj.remark=req.POST.get('remark')
        obj.amount=req.POST.get('amount')
        obj.catagory=req.POST.get('catagory')
        obj.user_id=uid
        obj.save()
        return redirect('/addExpenseRender')
    else:
        return render(req,"login.html")
    
def addIncomeRender(req):
    return render(req,"addincome.html")

def addIncomedata(req):
    if req.method=='POST' and 'id' in req.session:
        obj=Income()
        uid=req.session['id']
        obj.date=req.POST.get('date')
        obj.remark=req.POST.get('remark')
        obj.amount=req.POST.get('amount')
        obj.catagory=req.POST.get('catagory')
        obj.user_id=uid
        obj.save()
        return redirect('/addIncomeRender')
    else:
        return render(req,"login.html")
    


def allExpense(req):
    if 'id' in req.session:
        id=req.session['id']
        record=Expenses.objects.filter(user_id=id)
        if(record):
            listdata=record.values()
            return render(req,"allexpense.html",{"record":listdata})
        else:
            return render(req,"allexpense.html",{"msg":"record not found"})
    else:
        return render(req,"login.html")
    
def allIncome(req):
    if 'id' in req.session:
        id=req.session['id']
        record=Income.objects.filter(user_id=id)
        if(record):
            listdata=record.values()
            return render(req,"allincome.html",{"record":listdata})
        else:
            return render(req,"allincome.html",{"msg":"record not found"})
    else:
        return render(req,"login.html")
    

def logout(req):
    if 'id' in req.session:
        del req.session['id']
        del req.session['name']
        del req.session['img']
        return redirect('/')
    else:
        return redirect('/')
    
# def dashboardrender(req):
#     if 'id' in req.session:
#         id=req.session['id']
#         exp=Expenses.objects.filter(user_id=id)
#         inc=Income.objects.filter(user_id=id)
#         TotalExpense=0
#         TotalIncome=0


#         for x in exp:
#             TotalExpense=TotalExpense+(x.amount)
#         for x in inc:
#             TotalIncome=TotalIncome+(x.amount)
            
#         NETBALANCE=TotalIncome-TotalExpense
#         return render(req,"dashboard.html",{'total':"{}".format(NETBALANCE),'Inc':"{}".format(TotalIncome),'Exp':"{}".format(TotalExpense)})
    

from django.shortcuts import render
from .models import Expenses, Income

def dashboardrender(req):
    if 'id' in req.session:
        id = req.session['id']
        expenses = Expenses.objects.filter(user_id=id)
        income = Income.objects.filter(user_id=id)

        # Initialize totals
        TotalExpense = 0
        TotalIncome = 0

        # Expense categories
        expense_categories = {
            "Food": 0,
            "Clothes": 0,
            "Rent": 0,
            "Travel": 0,
            "Health":0
        }

        # Income categories
        income_categories = {
            "Salary": 0,
            "Share": 0,
            "Rent": 0,
            "Coaching": 0,
            "Cafe": 0
        }

        # Sum up expenses by category
        for expense in expenses:
            TotalExpense += expense.amount
            category = expense.catagory  # Assuming `category` is a field in your model
            if category in expense_categories:
                expense_categories[category] += expense.amount

        # Sum up income by category
        for inc in income:
            TotalIncome += inc.amount
            category = inc.catagory  # Assuming `category` is a field in your model
            if category in income_categories:
                income_categories[category] += inc.amount

        # Calculate net balance
        NETBALANCE = TotalIncome - TotalExpense

        # Prepare context for the template
        context = {
            "total": NETBALANCE,
            "Inc": TotalIncome,
            "Exp": TotalExpense,
            **expense_categories,  # Unpack expense categories
            **income_categories   # Unpack income categories
        }

        return render(req, "dashboard.html", context)
    else:
        return render(req, "login.html")  # Redirect if user not logged in





def passrender(req):
    return render(req,"c.html")

def npass(req):
    if req.method=='POST' and 'id' in req.session and 'name' in req.session and 'email' in req.session and 'contact' in req.session  :
        obj=User()
        uid=req.session['id']
        uname=req.session['name']
        uemail=req.session['email']
        ucontact=req.session['contact']
        img=req.session['img']
        
        upass=req.POST.get('password')
        data=User.objects.filter(password=upass)
        if(data):
            obj.password=req.POST.get('newpass')
            obj.img=img
            obj.id=uid
            obj.name=uname
            obj.email=uemail
            obj.contact=ucontact
            obj.save()
            return redirect('/')
        else:
            return render(req,"c.html",{'msg':'invalid password'})
            

    else:
        return HttpResponse("something went wrong")
        

       
def fpassrender(req):
    return render(req,"f.html")

def forgotpass(req):
    if req.method=='POST':
        obj=User()
        uname=req.POST.get('name')
        ucontact=req.POST.get('contact')
        data=User.objects.filter(name=uname,contact=ucontact)
        if(data):
            listData=data.values()
            uid=req.session['id']=listData[0]['id']
            req.session['name']=listData[0]['name']
            uemail=req.session['email']=listData[0]['email']
            req.session['contact']=listData[0]['contact']
            img=req.session['img']=listData[0]['img']
            obj.password=req.POST.get('newpass')
            obj.img=img
            obj.id=uid
            obj.name=uname
            obj.email=uemail
            obj.contact=ucontact
            obj.save()
            return render(req,'login.html')
        else:
            return render(req,'f.html',{'msg':'invalid data'})
    

            
          
    