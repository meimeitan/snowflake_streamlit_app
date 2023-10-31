import streamlit

streamlit.title('Asia Cafe Health Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔Hard-boiled Free-range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
##set the index as fruit
my_fruit_list = my_fruit_list.set_index('Fruit')

##Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
## to filter the table data
fruits_to_show = my_fruit_list.loc[fruits_selected]

##display the table on the page
streamlit.dataframe(fruits_to_show)


##new section to display fruityvice api response with header
streamlit.header('Fruityvice Fruit Advice!')

#add text entry box and ssend the input to fruityvice as part of API call
fruit_choice = streamlit.text_input('WHat fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

##new section to display fruityvice api response
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")


##normalise the json version of response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
##output shows in table
streamlit.dataframe(fruityvice_normalized)

#snowflake connector
import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)



