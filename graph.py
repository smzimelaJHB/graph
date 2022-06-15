from datetime import datetime
from termcolor import colored
import requests
import sys

BASE_URL = 'http://sam-user-activity.eu-west-1.elasticbeanstalk.com/'

class Graph:
    def __init__(this,api_endpoint):
        try:
            this.response=requests.get(api_endpoint)
        except requests.RequestException as e:
            this.error=e
            this.response={}

    def help(self):
        print("""Supported commands: 
                    start <date>
                    end <date>
                    help
              """)
        return False,''
    
    def is_integer(self,n):
        if(isinstance(n,int)):
            return True
        else:
            return False
        
    def is_date(self,api_dates,my_date):
        # check if date is available in the api
        api_dates.sort(key=lambda date:datetime.strptime(date, "%d-%m-%Y"))
        if(my_date in api_dates):
            return True
        else:
            print(f'Dates available from {api_dates[0]} to {api_dates[-1]}')
            return False
        
    def validate_date(self,date):
        split_date = date.split('-')
        day = split_date[0]
        month = split_date[1]
        year = split_date[2]
        
        conditions=[date[2]!='-',date[5]!='-',not self.is_integer(int(day)),
              not self.is_integer(int(month)),not self.is_integer(int(year)),
              int(day)>31,int(month)>12,int(day)<1,int(month)<1]

        try:
            # if all conditions are not0 met any will be false 
            if(not any(conditions)):
                return True
            else:
                return self.help()
                
        except Exception:
            print(colored("Invalid date entered!",'red'))
            return self.help()    
        
    def check_arguments(self,flags):
        if len(flags) > 1:
            if self.validate_date(flags[-1]):
                return True,flags
            else:
                return self.help()
        return False,''
        
    def get_api_info(self):
        # info=data
        info=self.response.json()
        list_info=sorted(info.items(), key=lambda x:x[1])
        sorted_info=dict(list_info)

        return sorted_info
    
    def do_reverse(self,isReversed):
        return isReversed
        
    def generate_x_values(self,values):
        return values
    
    def generate_y_values(self,keys):
        return keys
    
    def draw_x(self,x_values):
        # remove duplicates fro x_axis values
        x_values=list(set(x_values))
        # sort x values , so that it start with small values
        x_values=sorted(x_values)
        # add all values as string
        x_data=''.join([str(x)+" " for x in x_values])
        
        # add empty space above terminal and title into the center
        title="\n"+" "*int(len(x_data)/2)+colored(
        """Number of Active Users""","blue",attrs=['bold'])
        # combine title with x values
        x_data =title + colored('\n'+" "*12+x_data, attrs=['bold'])
        return x_data

    def draw_y(self,y_values):
        # adds new line and color to the dates
        y_data=['\n\n'+""+colored(y+"  ",'red',attrs=['bold']) for y in y_values]
        return y_data

    def draw_bar(self,bar_size=1):
        # set color to green for each bar
        return colored(bar_size*'*',"green",'on_green')
    
    def bar_length(self,sorted_x_data):
        space_length=[]
        # contains the value of x-axis 
        x_data=' '*12 #leave 12 spaces to the side 
        duplicates=[]
        
        for d in sorted_x_data:
            # if the length of a bar already exist copy it from duplicates
            # list and paste on our final list(space_length)    
            if d in duplicates:
                space_length.append(duplicates[duplicates.index(d)+1]-13)
                continue
            x_data+=str(d)+' '            
            #x space to dertemine the height of each bar 
            space_length.append(len(x_data)-13)
            # record duplicates so we can check in the next iteration
            duplicates.append(d)
            duplicates.append(len(x_data))
            
        return space_length
    
    def add_bars_to_y_axis(self,y_values,bar_size,isSort):
        # add values to a dictionary named y_values, values from bar_size list
        for cnt,elem in enumerate(bar_size):
            y_values[list(y_values.keys())[cnt]]=elem
        
        # store the keys as list from y_values dictionary
        list_y_values=list(y_values)
        # convert the list to date formate then sort it
        list_y_values.sort(key=lambda date:datetime.strptime(date, "%d-%m-%Y"))


        if(isSort[0] and isSort[1][-2]=='start'):
            if(self.is_date(list_y_values,isSort[1][-1])):
                list_y_values=list_y_values[list_y_values.index(isSort[1][-1])::]
            else:
                return
        if(isSort[0] and isSort[1][-2]=='end'):
            if(self.is_date(list_y_values,isSort[1][-1])):
                list_y_values=list_y_values[:list_y_values.index(isSort[1][-1])+1]
            else:
                return
        
        
        # adds new lines to y and format the text
        drawn_y=self.draw_y(list_y_values)
        # re-generate x coordinates values using keys from the sorted dates
        x_axis=[y_values[list_y_values[x]] for x in range(len(drawn_y))]
        # finally covert y axis to string adding bar length to the side
        y_data=''.join([y+self.draw_bar(x_axis.pop(0)) for y in drawn_y])
            
        return y_data
    
    def main(self):
        # api data
        api_dict=self.get_api_info()
        # handle command input
        isSort=self.check_arguments(sys.argv) 
        # Users
        x_axis=self.generate_x_values(list(api_dict.values()))
        
        draw_x=self.draw_x(list(x_axis))
        
        draw_y=self.add_bars_to_y_axis(api_dict,self.bar_length(x_axis),isSort) 
        # y axis
        if draw_y != None:
            print(draw_x,draw_y)

if __name__== "__main__" :
    graph=Graph(BASE_URL)
    graph.main()


    
    


            
            
            
    




