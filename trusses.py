import numpy as np

def truss_solver(node_matrix,node_load,node_constraints,adjacency_matrix,n):
    a=np.zeros([2*n,2*n],dtype=float) ## creating the coefficinent matrix of forces
    b=np.zeros(2*n,dtype=float) 
    k=0
    l=0
    vis=np.zeros([n,n],dtype=int) ## creating the visited nodes matrix
    for i in range(0,2*n,2):
        if(node_constraints[(int)(i/2)][0]==0):  ## Applying the constraints conditions
            a[i][k]=1.0
            k=k+1
        if(node_constraints[(int)(i/2)][1]==0):  ## Applying the constraints conditions
            a[i+1][k]=1.0
            k=k+1
        for j in range(n):
            if(adjacency_matrix[(int)(i/2)][j]==1 and vis[(int)(i/2)][j]==0):
                x=node_matrix[j][0]-node_matrix[(int)(i/2)][0]
                y=node_matrix[j][1]-node_matrix[(int)(i/2)][1]
                len=np.sqrt(x**2+y**2)  ## calculating the beam length
                cos=x/len     ## calculating the cosine angle of beam with horizontal
                sin=y/len     ## calculating the sine angle of beam with vertical
                if(i!=2*n-2):
                    if(vis[j][(int)(i/2)]==0): 
                        a[i][k]=cos         ## entering coefficients in coefficient matrix
                        a[i+1][k]=sin       ## entering coefficients in coefficient matrix
                        vis[(int)(i/2)][j]=k
                        k=k+1
                    elif(vis[j][(int)(i/2)]!=0):
                        a[i][vis[j][(int)(i/2)]]=cos   ## entering coefficients in coefficient matrix
                        a[i+1][vis[j][(int)(i/2)]]=sin    ## entering coefficients in coefficient matrix
                        vis[(int)(i/2)][j]=vis[j][(int)(i/2)]    ## marked visited in visited matrix
                else:
                    a[i][vis[j][(int)(i/2)]]=cos  ## entering the coefficients in coefficient matrix
                    a[i+1][vis[j][(int)(i/2)]]=sin  ## entering coefficients in coefficient matrix
                    vis[(int)(i/2)][j]=vis[j][(int)(i/2)]   ## marked visited in visited matrix
        b[l]=node_load[(int)(i/2)][0]   
        b[l+1]=node_load[(int)(i/2)][1]
        l=l+2
    print(a) ## printing the coefficient matrix
    list=-1*np.linalg.solve(a,b)
    for v in range(2*n):
        print((int(list[v]*(1000)))/1000) ## printing the results matrix

n=5  ## number of nodes
node_matrix = np.array([[0,0],[4,0],[8,0],[12,7],[4,7]]) ## coordinates of nodes
node_load=np.array([[0,0],[0,0],[0,0],[0,0],[0,-200]])  ## loads on nodes
node_constraints=np.array([[0,0],[1,1],[1,0],[1,1],[1,1]]) ## constraints on nodes
adjacency_matrix=np.array([ [0,1,0,0,1],
                            [1,0,1,0,1],
                            [0,1,0,1,1],    ## connection nodes
                            [0,0,1,0,1],
                            [1,1,1,1,0],
                            ])
truss_solver(node_matrix,node_load,node_constraints,adjacency_matrix,n) ## solving the trusses