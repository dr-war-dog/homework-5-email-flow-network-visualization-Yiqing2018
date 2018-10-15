![](https://ws1.sinaimg.cn/large/006tNbRwly1fvh59oez3dj304t04uaap.jpg)
# Homework 5: Email Flow Network Visualization

|Author|Yiqing Liu|
|---|---
|E-mail|yiqing5@:corn:.edu

### Requirements
- Make use of any network analysis visualizations
- Do not use more dimensions (color, shape, size, etc.) than you need. Having circles appear both larger and darker due to more divisiveness is redundant.
- Convey only relevant information – think of the message your graphic is meant to present; for each piece of information, ask yourself if the graphic would work equally well without!

****

### data preprocessing
take a look at our data (personal.csv)
- "date" column, convert to date formate  

```
			time=datetime.datetime.strptime(df['date'][i], '%Y-%m-%dT%H:%M:%S.000Z').date()
```

- the length of "receiver","sender" value is too large, so we take the first word of email address as sender ID and receiver ID. It makes sense  
i.e pariatur.officiis.officiis.et@nihil.bogisich.info(email address) belongs to pariatur(person)  
```
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
```

****

### thisday, somedays
We are interested in email info on specific day or during a time period.  
implement functions to get rid of irrelevant information:
```
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
```

```
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
```

### Networkx  

#### simple Network Graph  
ignore duplicate edges, we don't care frequency. We just want to know who are sending emails to whom.
![](https://ws3.sinaimg.cn/large/006tNbRwly1fw5f09e5fzj31kw11xdjy.jpg)
![](https://ws1.sinaimg.cn/large/006tNbRwly1fw5f14ssrwj31kw11xgtd.jpg)  

#### directed Graph
we care about who are sending emails to whom, there are arrows pointing from source to target  
![](https://ws1.sinaimg.cn/large/006tNbRwly1fw5f2wv1e9j31kw11xqco.jpg)  

#### Muti Graphs
we care about the frequency. {(A,B),(A,C),(A,B)} "record duplicates"
![](https://ws3.sinaimg.cn/large/006tNbRwly1fw5f4xdjqrj31kw11xgwe.jpg)

#### weighed Graphs
we assume 'to' type emailas are different from 'cc' type emails.  
```
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
```
![](https://ws2.sinaimg.cn/large/006tNbRwly1fw5f5y3v3aj31kw11x45f.jpg)

****
