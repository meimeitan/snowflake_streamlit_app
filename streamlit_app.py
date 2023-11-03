import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Asia Cafe Health Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔Hard-boiled Free-range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
##set the index as fruit
my_fruit_list = my_fruit_list.set_index('Fruit')

##Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
## to filter the table data
fruits_to_show = my_fruit_list.loc[fruits_selected]

##display the table on the page
streamlit.dataframe(fruits_to_show)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return streamlit.dataframe(fruityvice_normalized)
    
##new section to display fruityvice api response with header
streamlit.header('Fruityvice Fruit Advice!')
try:
#add text entry box and ssend the input to fruityvice as part of API call
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
#streamlit.write('The user entered', fruit_choice)
    if not fruit_choice:
         streamlit.error("Please select a fruit to get information.")
    else:
         back_from_function = get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()
  
#don't run anything past here while we troubleshoot
streamlit.stop()

#snowflake connector
#import snowflake.connector
streamlit.header("The fruit load list contains:")
#snowflake-related functions:
def get_fruit_load_list():
    with my_cnx_cursor() as my_cur:
         my_cur.execute("SELECT * from fruit_load_list")
         return my_cur.fetchall()

#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#add text entry box and send the input to snowflake connector as part of API call
fruit_choice2 = streamlit.text_input('What fruit would you like add?', 'jackfruit')
streamlit.write('Thanks for adding ', fruit_choice2)

##This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")


