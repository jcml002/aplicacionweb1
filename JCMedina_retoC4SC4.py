import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng
import plotly.express as px

#Lee el archivo
df=pd.read_csv("Employee_data.csv")

st.title("Socialize your knowledge")
st.subheader(":bar_chart: _Pagina Web para analizar el desempeño de los colaboradores del Área de Marketing_ ",  divider=True)

#Configura la barra lateral
st.sidebar.image("Logo02.jpg")


#Filtros
st.sidebar.header("FILTROS: ")
performance_score= st.sidebar.multiselect("Puntaje de desempeño:",
                                          options=df['performance_score'].unique(),
                                          default=df['performance_score'].unique())
                                          

gender = st.sidebar.multiselect("Genero:",
                                options=df['gender'].unique(),
                                default=df['gender'].unique())

marital_status = st.sidebar.multiselect(
    "Estado Civil:",
    df['marital_status'].unique(),
	default=df['marital_status'].unique(),
    max_selections=5,
    accept_new_options=False,
)

#Aplicar los filtros seleccionados por el usuario
df_selection=df.query("gender == @gender & performance_score == @performance_score & marital_status == @marital_status")


#GRAFICAS
#Distribución de los puntajes de desempeño
df_performance=df_selection['performance_score']

fig_perf_dist = px.histogram(df_performance, 
                   x='performance_score', 
                   title='Distribución de los puntajes de desempeño',
                   labels={'performance_score': 'Puntaje de desempeño', 'count': 'Cantidad'},
                   color_discrete_sequence=["#7E99CB"],
                   text_auto=True
)
st.plotly_chart(fig_perf_dist)

st.divider()

#Promedio de horas trabajadas por el género del empleado.
avg_hours_gender=(
    df_selection[['gender','average_work_hours']].groupby('gender').mean().reset_index())

fig_hours_gender=px.bar(avg_hours_gender,
                        x='gender',
                        y="average_work_hours", 
                        orientation="v",
                        title="Promedio de horas trabajadas por género",
                        labels={"gender": "Género", "average_work_hours": "Horas trabajadas"},
                        color_discrete_sequence=["#7E99CB"],
                        template="plotly_white", text_auto=True)

fig_hours_gender.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_hours_gender)
st.divider()
#Edad de los empleados con respecto al salario de los mismo.
fig_age_salary = px.scatter(
    df_selection,
    x="age",
    y="salary",
    title="Relación entre Edad y Salario",
    labels={"age": "Edad", "salary": "Salario"},
    color_discrete_sequence=["#7E99CB"],
    template="plotly_white"
)
fig_age_salary.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_age_salary)
st.divider()
#Promedio de horas trabajadas por puntaje de desempeño
avg_hours_performance = (
    df_selection.groupby('performance_score')['average_work_hours'].mean().reset_index()
)

fig_hours_performance = px.bar(
    avg_hours_performance,
    x='performance_score',
    y='average_work_hours',
    title="Promedio de horas trabajadas vs Puntaje de desempeño",
    labels={"performance_score": "Puntaje de desempeño", "average_work_hours": "Horas trabajadas"},
    color_discrete_sequence=["#7E99CB"],
    template="plotly_white",
    text_auto=True
)
fig_hours_performance.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_hours_performance)

#Conclusiones
st.subheader(":bookmark_tabs: _Conclusiones:_ ",  divider=True)

st.info("Sin importar el género la mayoría de los empleados tiene un puntaje alto de desempeño, lo cual indica un buen rendimiento laboral en general.")
st.info("La relación en horas trabajadas y el género los promedios son equitativos respecto a las cargas.")
st.info("Respecto a las a la edad y salario de los empleados, vemos una ligera tendencia a salarios mayores en empleados de más edad, esto puede deberse con el nivel del puesto y/o la experiencia laboral.")
st.info("La relación del promedio de horas trabajadas versus el puntaje de desempeño muestra un ligero aumento de horas trabajadas los que tienen más puntaje de desempeño, en general.")
