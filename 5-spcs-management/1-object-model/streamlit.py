# Snowpark Container Manager
# paste into a new Streamlit app online file
# to work, grant any role creating services to SYSADMIN

import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(layout="wide")
st.title("Snowpark Container Manager")
session = get_active_session()

if "repos" not in st.session_state:
    st.session_state["repos"] = \
        session.sql("show image repositories").collect()
if "pools" not in st.session_state:
    st.session_state["pools"] = \
        session.sql("show compute pools").collect()
if "services" not in st.session_state:
    st.session_state["services"] = \
        session.sql("show services").collect()
if "snapshots" not in st.session_state:
    st.session_state["snapshots"] = \
        session.sql("show snapshots").collect()

def get_desc(query):
    df = session.sql(query).collect()
    desc = pd.DataFrame(df).transpose()
    desc.columns = ["value"]
    return desc;
    
def get_repo(repos):
    list = [f'{row["database_name"]}.{row["schema_name"]}.{row["name"]}'
        for row in repos]
    return st.sidebar.selectbox(
        "Repository", list, label_visibility="collapsed")
    
def show_repo(repo):
    if repo is None or repo == '':
        st.info(f'No Repository Selected.')
        return;

    st.subheader(f'Repository: {repo}')
    parts = str(repo).split('.')
    query = (f"show image repositories like '{parts[2]}'"
        + f" in schema {parts[0]}.{parts[1]}")
    desc = get_desc(query)

    query = f"show images in image repository {repo}"
    images = session.sql(query)
    
    tabs = st.tabs(["Properties", "Images"])
    tabs[0].dataframe(desc, use_container_width=True)
    tabs[1].dataframe(images, use_container_width=True)

def get_pool(pools):
    list = [row["name"] for row in pools]
    return st.sidebar.selectbox(
        "Pool", list, label_visibility="collapsed")
    
def show_pool(pool):
    if pool is None or pool == '':
        st.info(f'No Pool Selected.')
        return;

    st.subheader(f'Pool: {pool}')
    query = f"desc compute pool {pool}"
    desc = get_desc(query)
    
    tabs = st.tabs(["Properties"])

    try:
        cols = tabs[0].columns(5)
        suspend = cols[0].button("Suspend", use_container_width=True)
        resume = cols[1].button("Resume", use_container_width=True)
        stopall = cols[2].button("Stop All", use_container_width=True)
        if suspend:
            session.sql(f"alter compute pool {pool} suspend").collect()
        elif resume:
            session.sql(f"alter compute pool {pool} resume").collect()
        elif stopall:
            session.sql(f"alter compute pool {pool} stop all").collect()
    except Exception as e:
        tabs[0].error(e.args[0])

    tabs[0].dataframe(desc, use_container_width=True)

def get_service(services):
    list = [f'{row["database_name"]}.{row["schema_name"]}.{row["name"]}'
        for row in services]
    return st.sidebar.selectbox(
        "Service", list, label_visibility="collapsed")
    
def show_service(service):
    if service is None or service == '':
        st.info(f'No Service Selected.')
        return;

    st.subheader(f'Service: {service}')
    tabs = st.tabs([
        "Properties",
        "Endpoints",
        "Containers",
        "Instances",
        "Roles"])
    
    try:
        cols = tabs[0].columns(5)
        suspend = cols[0].button("Suspend", use_container_width=True)
        resume = cols[1].button("Resume", use_container_width=True)
        if suspend:
            session.sql(f"alter service {service} suspend").collect()
        elif resume:
            session.sql(f"alter service {service} resume").collect()
    except Exception as e:
        tabs[0].error(e.args[0])

    try:
        tabs[0].dataframe(
            get_desc(f"desc service {service}"),
            use_container_width=True)
        tabs[1].dataframe(
            session.sql(f"show endpoints in service {service}"),
            use_container_width=True)
        tabs[2].dataframe(
            session.sql(f"show service containers in service {service}"),
            use_container_width=True)
        tabs[3].dataframe(
            session.sql(f"show service instances in service {service}"),
            use_container_width=True)
        tabs[4].dataframe(
            session.sql(f"show roles in service {service}"),
            use_container_width=True)
    except Exception as e:
        tabs[0].error(e.args[0])

def get_snapshot(snapshots):
    list = [f'{row["database_name"]}.{row["schema_name"]}.{row["name"]}'
        for row in snapshots]
    return st.sidebar.selectbox(
        "Snapshots", list, label_visibility="collapsed")
        
def show_snapshot(snapshot):
    if snapshot is None or snapshot == '':
        st.info(f'No Snapshot Selected.')
        return;

    st.subheader(f'Snapshot: {snapshot}')
    query = f"desc snapshot {snapshot}"
    desc= get_desc(query)

    tabs = st.tabs(["Properties"])
    tabs[0].dataframe(desc, use_container_width=True)


opts = ["All", "Repository", "Pool", "Service", "Snapshot"]
type = st.sidebar.radio("Object Type", opts)

if type == opts[1]:
    repo = get_repo(st.session_state["repos"])
    show_repo(repo)

elif type == opts[2]:
    pool = get_pool(st.session_state["pools"])
    show_pool(pool)

elif type == opts[3]:
    service = get_service(st.session_state["services"])
    show_service(service)
    
elif type == opts[4]:
    snapshot = get_snapshot(st.session_state["snapshots"])
    show_snapshot(snapshot)

else:
    tabs = st.tabs([
        "Repositories",
        "Pools",
        "Services",
        "Snapshots"])
    tabs[0].dataframe(
        st.session_state["repos"],
        use_container_width=True)
    tabs[1].dataframe(
        st.session_state["pools"],
        use_container_width=True)
    tabs[2].dataframe(
        st.session_state["services"],
        use_container_width=True)
    tabs[3].dataframe(
        st.session_state["snapshots"],
        use_container_width=True)
