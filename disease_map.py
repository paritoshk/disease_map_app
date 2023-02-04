from email.policy import default
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis.network import Network

st.set_page_config(page_icon="🧬 ", page_title="Disease_map", layout="wide")
from helper_tools.text_processing import findnonNAinColumn, change_none_to_string
st.title("🧬  Disease Map")

  
def findnonNAinColumn(df, column):
    """ a function that finds non NA values in a column"""
    return (df[~df[column].isnull()]).reset_index(drop=True)

# Read dataset (CSV)
#final_network_map = pd.read_csv("data/final_network_map" + '.bz2', \
                                             #compression='bz2')
#final_network_map =final_network_map.head(100)

final_network_map = pd.read_csv('data/df_disease.csv', index_col=0)

# Set header title
st.header("An interactive disease agnostic network map")
st.subheader("This map lets you explore between total 799 diseases and 45K relationships of 8 types between 36k nodes of five types")

#st.header('Select Free Text or Pre-loaded search')
#selected_functions = st.selectbox('Free-text feature coming soon', ['Pre-loaded search'])  # 'Free Text',
#st.write("You selected: " + selected_functions)

st.sidebar.write("Options other than Disease type are coming up soon!")
node_type_select = st.sidebar.multiselect('Select a node type', ['Disease',
 'Compound',
 'Anatomy',
 'Molecular Function',
 'Pathway',
 'Side Effect',
 'Cellular Component',
 'Biological Process',
 'Gene',
 'Symptom'],default=['Disease'])
st.sidebar.write("You selected: " + ", ".join(node_type_select))

edge_type_select = st.sidebar.multiselect('Select an edge type',list(set(final_network_map['metaedge'])),default = [ 'Disease - resembles - Disease'])
st.sidebar.write("You selected: " + ", ".join(edge_type_select))



# df_interact.columns = ['Source','Target','Function']

# Function that takes streamlit input of user selection bween companies and holders"""

# take user input to make the database Filers and holdings could be interchanged so therefore - a radio button to
# choose between whether to choose a holder or comapnies User selection between companies and holders


# Set info message on initial site load
if len(node_type_select) == 0 or len(edge_type_select) == 0:
    st.sidebar.text('Choose at least 1 node type or edge type to start')

# Create network graph when user selects >= 1 item
else:
    df_interact = final_network_map[final_network_map['kind_of_target'].isin(node_type_select)]
    df_interact = df_interact[df_interact['metaedge'].isin(edge_type_select)]
    entity_list = list(set(df_interact['source_name'].tolist() + df_interact['target_name'].tolist()))

    selected_objs = st.sidebar.multiselect('Select objects to visualize', entity_list,default = ['schizophrenia',"Alzheimer's disease"])
# Set info message on initial site load
if len(selected_objs) == 0:
    st.sidebar.text('Choose at least 1 object to start')
    



# Create network graph when user selects >= 1 item
else:
    dict_colors = {'Disease':'green','Gene':'orange','Compound':'skyblue','Pathway':'pink','Symptom':'red'}
    st.dataframe(pd.DataFrame.from_dict(dict_colors, orient='index', columns=['color']))
    df_select = df_interact.loc[df_interact['source_name'].isin(selected_objs) | \
                                df_interact['target_name'].isin(selected_objs)]
    df_select = df_select.reset_index(drop=True)
    # st.table(df_legend)
    st.sidebar.header('Disease Map')
    st.sidebar.subheader('Hover over the arrow to see type of interaction')

    # Create A network object in Pyvis
    got_net = Network(
        height='720px',
        width='1280px',
        bgcolor='#00172B',
        font_color='white',
        directed=False,

    )

    # Create networkx graph object from pandas dataframe

    got_net.barnes_hut()
    got_data = df_select

    sources = got_data['source_name']
    targets = got_data['target_name']
    edge_name = got_data['metaedge']
    kind_of_target = got_data['kind_of_target']
    kind_of_source = got_data['kind_of_source']
    edge_data = zip(sources, targets, edge_name, kind_of_target, kind_of_source)
    for e in edge_data:
        src = e[0]
        dst = e[1]
        edge_name= e[2]
        kind_of_target = e[3]
        kind_of_source = e[4]
        
        if kind_of_target == 'Disease':
            got_net.add_node(src,  label=src, title= kind_of_source, color='green')
            got_net.add_node(dst,  label=dst, title = kind_of_target, color='white')


        elif kind_of_target == 'Gene':
            got_net.add_node(src,  label=src, title= kind_of_source,  color='orange')
            got_net.add_node(dst,  label=dst,title = kind_of_target, color='white')

        elif kind_of_target == 'Compound':
            got_net.add_node(src,  label=src,title= kind_of_source,  color='skyblue')
            got_net.add_node(dst,  label=dst,title = kind_of_target, color='white')


        elif kind_of_target == 'Pathway':
            got_net.add_node(src,  label=src, title= kind_of_source, color='pink')
            got_net.add_node(dst,  label=dst, title = kind_of_target,color='white')


        elif kind_of_target == 'Symptom':
            got_net.add_node(src,  label=src,title= kind_of_source,  color='red')
            got_net.add_node(dst, label=dst,title = kind_of_target, color='white')
        else:

            got_net.add_node(src, label=src,title = kind_of_source, color='yellow')
            got_net.add_node(dst, label=dst, title = kind_of_target, color='blue')




        try:
            got_net.add_edge(src, dst,title="Type " + str(edge_name))  # add size as shares changed interger value, add also percentage ownershp and its change %
        except:
            got_net.add_edge(src,dst)  # add size as shares changed interger value, add also percentage ownershp and its change %

 
    # Generate network with specific layout settings
    got_net.repulsion(
                        node_distance=620,
                        central_gravity=0.43,
                        spring_length=140,
                        spring_strength=0.130,
                        damping=0.945
        
                       )

    got_net.save_graph('disease_net_graph.html')
    HtmlFile = open('disease_net_graph.html', 'r', encoding='utf-8')
    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=800,width=1300,scrolling=True)

#put expander 
st.subheader('Instructions:')
with st.expander("Click Here"):
    st.write('1. Toggle/Optional - Select between connection type and node type')
    st.write('2. Type a name of gene or disease or compound or pathway or symptom in the search bar')
    st.write('3. Hover over each node to see what type of node it is and each edge to see the type of connection')

page_bg_img = """
<style>
.stApp {
background-image: url("https://images.unsplash.com/photo-1576086213369-97a306d36557?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1480&q=80");
background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
