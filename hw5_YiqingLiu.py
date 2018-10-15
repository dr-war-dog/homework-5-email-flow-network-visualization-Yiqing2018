import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import datetime

class nx_drawGraph:
	def __init__(self,filepath,column1,column2,column3):
		self.df=pd.read_csv(filepath)
		# print(self.df.dtypes)
		self.column1=column1
		self.column2=column2
		self.column3=column3
		self.index=1
	def get_df(self):
		return self.df
	def short_label(self,df):
		for i in range(df[self.column1].size):
			cell1=df[self.column1][i]
			temp1=str(cell1)
			name1=temp1.split('.')[0]
			df.loc[i,self.column1]=name1
			cell2=df[self.column2][i]
			temp2=str(cell2)
			name2=temp2.split('.')[0]
			df.loc[i,self.column2]=name2

	def thisday(self,df,column_name,y,m,d):
		this_day=datetime.date(y,m,d)
		newdf=pd.DataFrame(columns=('idx',self.column1,self.column2,self.column3))
		for i in range(df[self.column1].size):
			time=datetime.datetime.strptime(df['date'][i], '%Y-%m-%dT%H:%M:%S.000Z').date()
			if(time==this_day):
				newdf=newdf.append({self.column1:self.df[self.column1][i],self.column2:df[self.column2][i],self.column3:df[self.column3][i]},ignore_index=True)
		title=str(y)+"-"+str(m)+"-"+str(d)+" Network Graph"
		self.short_label(newdf)
		self.simple_graph(newdf,title+" (undirected, springlayout)")	
		return newdf

	def somedays(self,df,column_name,start_y,start_m,start_d,end_y,end_m,end_d):
		start_day=datetime.date(start_y,start_m,start_d)
		end_day=datetime.date(end_y,end_m,end_d)
		newdf=pd.DataFrame(columns=(self.column1,self.column2,self.column3))
		for i in range(df[self.column1].size):
			date=datetime.datetime.strptime(self.df['date'][i], '%Y-%m-%dT%H:%M:%S.000Z').date()
			if(date>=start_day and date<=end_day):
				newdf=newdf.append({self.column1:self.df[self.column1][i],self.column2:df[self.column2][i],self.column3:df[self.column3][i]},ignore_index=True)
		title="From "+str(start_y)+"-"+str(start_m)+"-"+str(start_d)+" to "+str(end_y)+"-"+str(end_m)+"-"+str(end_d)+" Network Graph"
		self.short_label(newdf)
		self.simple_graph(newdf,title+" (undirected, springlayout)")
		self.directed_graph(newdf,title+" (directed, shell layout)")
		self.Multi_graph(newdf,title+" (Multi, random layout)")
		self.Weighed_graph(newdf,title+" (weighed,kamada kawai layout)")
		return newdf

	def Multi_graph(self,df,title):
		G= nx.from_pandas_edgelist(df,self.column1,self.column2,
			create_using=nx.MultiGraph())
		# print(G.edges)
		plt.figure(figsize=(30,20))
		plt.title(title,fontsize=60)
		pos=nx.random_layout(G)
		nx.draw(G,with_labels=True,
			font_size=25,node_size=1000,node_color=['blue','pink','red','green','orange','yellow','purple'],pos=pos)
		# plt.show()
		plt.tight_layout()
		plt.savefig(str(self.index)+'.png')
		self.index=self.index+1

	def Weighed_graph(self,df,title):
		plt.figure(figsize=(30,20))
		plt.title(title,fontsize=50)
		text= "Bule line: to\nGrey line: cc\n"
		plt.text(-1, -1, text,fontsize=40,bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))

		G=nx.Graph()

		for i in range(df[self.column3].size):
			send_type=df[self.column3][i]
			source=str(df[self.column1][i])
			# print(source)
			target=str(df[self.column2][i])
			# print(target)
			if(send_type=='cc'):
				G.add_edge(source,target,color='grey',weight='2')
			else:
				G.add_edge(source,target,color='blue',weight='5')
		# plt.show()
		pos = nx.circular_layout(G)
		edges = G.edges()
		colors = [G[u][v]['color'] for u,v in edges]
		weights = [G[u][v]['weight'] for u,v in edges]
		pos=nx.kamada_kawai_layout(G,weight=1)
		nx.draw(G,edges=edges, edge_color=colors, width=weights,pos=pos,
			with_labels=True,font_size=20,node_size=1000,
			node_color=['blue','pink','red','green','orange','yellow','purple'])
		plt.savefig(str(self.index)+'.png')
		self.index=self.index+1


	def directed_graph(self,df,title):
		G = nx.from_pandas_edgelist(df,source=self.column1,target=self.column2,
			create_using=nx.DiGraph())

		plt.figure(figsize=(30,20))
		plt.title(title,fontsize=60)
		pos=nx.shell_layout(G)
		nx.draw(G,with_labels=True,width=2,
			font_size=25,node_size=1000,
			node_color=['blue','pink','red','green','orange','yellow','purple'],pos=pos)
		# plt.show()
		plt.savefig(str(self.index)+'.png')
		self.index=self.index+1
		
	def simple_graph(self,df,title):
		G = nx.from_pandas_edgelist(df,self.column1,self.column2)
		# print(G.edges)
		plt.figure(figsize=(30,20))
		plt.title(title,fontsize=60)
		pos=nx.spring_layout(G)
		nx.draw(G,with_labels=True,width=3,
			font_size=25,node_size=1000,node_color=['blue','pink','red','green','orange','yellow','purple'],pos=pos)
		# plt.show()
		plt.tight_layout()
		plt.savefig(str(self.index)+'.png')
		self.index=self.index+1


def main():
	dg=nx_drawGraph("personal.csv",'sender','receiver','type')
	origin_df=dg.get_df()
	dg.thisday(origin_df,'date',2006,5,15)
	somedays_df=dg.somedays(origin_df,'date',2006,2,1,2006,5,1)


if __name__=='__main__':
	main()