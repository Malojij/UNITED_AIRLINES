
from graphviz import Digraph

# Create a flowchart using Graphviz
dot = Digraph(format='png', graph_attr={'rankdir': 'LR', 'bgcolor': 'lightgrey', 'labeljust': 'l', 'fontsize': '20'}, node_attr={'style': 'filled', 'fontname': 'Helvetica'})

# Define nodes with different colors
dot.node('A', 'Merchant initiates PTR request', fillcolor='lightblue')
dot.node('B', 'Payment Page Displayed', fillcolor='lightgreen')
dot.node('C', 'Page Submitted\n(Payment Data Tokenized & Authorization Initiated)', fillcolor='orange')
dot.node('D', 'Merchant Backend Notified\n(Token & Authorization Response)', fillcolor='gold')
dot.node('E', 'Merchant Initiates Authorization using Token', fillcolor='lightcoral')
dot.node('F', 'Authorization Response Received', fillcolor='lightpink')
dot.node('G', 'Transaction Status Request from Merchant', fillcolor='lightyellow')
dot.node('H', 'Aurus Posts Callback to Merchant', fillcolor='violet')
dot.node('I1', 'Callback Approved', fillcolor='mediumseagreen')
dot.node('I2', 'Callback Timeout\n→ Reversal by Aurus', fillcolor='tomato')
dot.node('I3', 'Callback Declined\n→ Reversal by Aurus', fillcolor='tomato')
dot.node('J', 'Additional Processes:\nPre-Auth, Post-Auth, Refund, Void\n(With API Flows & Screenshots)', fillcolor='cyan')

# Define edges
dot.edges([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'H')])
dot.edge('H', 'I1')
dot.edge('H', 'I2')
dot.edge('H', 'I3')
dot.edge('F', 'J', label='Also includes...')

# Render diagram
dot.render('merchant_payment_flow_diagram', cleanup=False)
