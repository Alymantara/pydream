import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pylab as plt
import os.path
import glob

class pydream:

	def __init__(self,clean_input=True):
		'''
		The default parameters are given below. First up are the global non-fitted input parameters.
		Second are the global fitted parameters whos starting values can be modified below.
		Note that...
		1) Entering zero step sizes indicates the parameter will not be stepped)
		2) Light curve-specific parameters (the error bar scaling, starting lag centroids and widths
		for line light curves etc) are specified in the add_lc function.
		'''


		#config, path, compiler parameters
		self.module_path = "/data/jvhs1/dream/"
		self.exec_file = 'dream.exe'
		print('DREAM path... ' + self.module_path)
		
		merger_dirs = glob.glob('./dream_merger_*/')
		if len(merger_dirs) == 0: 
			os.system("mkdir dream_merger_00")
			self.workdir = "./dream_merger_00/"
		else:
			merger_dirs = np.sort(merger_dirs)
			last = np.int(merger_dirs[-1][-3:-1])
			os.system("mkdir dream_merger_"+str(last+1).zfill(2))
			self.workdir = "./dream_merger_"+str(last+1).zfill(2)+"/"

		self.dt = 0.1
		self.roa = 'C'
		self.hw = 1.0
		self.nits = 1000

		self.agn = 'AGN'
		self.list = self.agn+'.lis'

		lis = open(self.workdir+self.list,'a')
		lis.write('# filter scope datafile\n')
		lis.close()

		if clean_input:
			os.system('rm '+self.workdir+self.list)
		self.df2 = {}
		self.ctr = 0
		self.band = 'X'

		self.input_lcs = {}

	def run(self):
		self.lc_names = self.input_lcs.Tel.unique()
		self.make_param_file()
		#print(self.workdir+'./dream '+self.param_file)
		os.system('cp '+self.module_path+self.exec_file+' '+self.workdir+'/.')
		os.chdir(self.workdir)
		#print(os.pwd())
		os.system('./dream.sh')
		os.chdir('..')
		#   Col 1 : HJD
		#   Col 2 : flux
		#   Col 3 : rms statistical error
		#   Col 4 : rms systematic error
		#   Col 5 : scope (see key below)
		#   Col 6 : add
		#   Col 7 : scl

		#self.read_out(self.workdir+self.agn+'_'+self.band+'_dream.dat')


	def add_lc(self,telescope,data):

		lc_name = self.band+'_'+telescope+'.dat'
		pf = open(self.workdir+lc_name,'w')
		lis = open(self.workdir+self.list,'a')
		lis.write(self.band+' '+telescope+' '+lc_name+'\n')
		lis.close()
		ndata = data.shape[0]
		for i in range(ndata):
			pf.write("{:12.6f} {:8.3f} {:8.3f}\n".format(data[i][0],data[i][1],data[i][2]))
			self.df2[self.ctr] = {'MJD': data[i][0], 
					'Flux': data[i][1],
					'Error': data[i][2],
					'Tel': telescope,
					}

			self.ctr += 1
		pf.close()

		self.input_lcs = pd.DataFrame.from_dict(self.df2,"index")

	def read_out(self,location):
		self.ouptput_lcs = pd.read_csv(location,
				delim_whitespace=True,
				names=['MJD','Flux','Error_stat',
						'Error_sys','tel','add','scl'])

	def make_param_file(self):

		pf = open(self.workdir+'dream.sh','w')

		pf.write("# shell script runs dream on F9 B data\n")
		pf.write("# 2020 Jun Keith Horne @ St Andrews\n")
		pf.write("\n")
		#pf.write("set dt = {}\n".format(self.dt))
		#pf.write("set roa = {}\n".format(self.roa))
		#pf.write("set hw = {}\n".format(self.hw))
		#pf.write("\n")
		#pf.write("set nits = {}\n".format(self.nits))
		#pf.write("\n")
		#pf.write("set agn = {}\n".format(self.agn))
		#pf.write("\n")
		#pf.write("set infile = {}\n".format(self.list))
		#pf.write("set plotx = $agn'_dream_x.ps'\n")
		#pf.write("set plotlc = $agn'_dream_lc.ps'\n")
		pf.write("\n")
		pf.write("date\n")
		pf.write("./dream.exe << $\n")
		pf.write("\n")
		pf.write("d\n")
		pf.write("{}\n".format(self.list))
		pf.write("{}\n".format(self.dt))
		pf.write("{}\n".format(self.roa))
		pf.write("{}\n".format(self.hw))
		pf.write("\n")
		pf.write("i\n")
		pf.write("{}\n".format(self.nits))
		pf.write("\n")
		pf.write("	! convergence plot\n")
		pf.write("x\n")
		pf.write("c\n")
		pf.write("{}\n".format(self.agn+'_dream_x.ps'))
		pf.write("u\n")
		pf.write("p\n")
		pf.write("n\n")
		pf.write("n\n")
		pf.write("\n")
		pf.write("	! lightcurve plot\n")
		pf.write("l\n")
		pf.write("c\n")
		pf.write("{}\n".format(self.agn+'_dream_lc.ps'))
		pf.write("u\n")
		pf.write("p\n")
		pf.write("n\n")
		pf.write("n\n")
		pf.write("\n")
		pf.write("	! output\n")
		pf.write("o\n")
		pf.write("{}\n".format(self.agn))
		pf.write("\n")
		pf.write("\n")
		pf.write("q\n")
		pf.write("\n")
		pf.write("$\n")
		pf.write("date\n")
		pf.close()
		os.system('chmod 777 '+self.workdir+'dream.sh')


class pydreamgrid:

	def __init__(self,clean_input=True):
		'''
		The default parameters are given below. First up are the global non-fitted input parameters.
		Second are the global fitted parameters whos starting values can be modified below.
		Note that...
		1) Entering zero step sizes indicates the parameter will not be stepped)
		2) Light curve-specific parameters (the error bar scaling, starting lag centroids and widths
		for line light curves etc) are specified in the add_lc function.
		'''


		#config, path, compiler parameters
		self.module_path = "/data/jvhs1/dream/"
		self.exec_file = 'dream.exe'
		print('DREAM path... ' + self.module_path)
		
		merger_dirs = glob.glob('./dream_merger_*/')
		if len(merger_dirs) == 0: 
			os.system("mkdir dream_merger_00")
			self.workdir = "./dream_merger_00/"
		else:
			merger_dirs = np.sort(merger_dirs)
			last = np.int(merger_dirs[-1][-3:-1])
			os.system("mkdir dream_merger_"+str(last+1).zfill(2))
			self.workdir = "./dream_merger_"+str(last+1).zfill(2)+"/"

		self.dt = 0.1
		self.roa = 'C'
		self.hw = 1.0
		self.nits = 1000

		# grid variables
		self.grid1 = 0.25
		self.grid2 = 8.
		self.ngrid = 9

		# iterations per grid point (before and after recenter and expand)
		self.nits1 = 100
		self.nits2 = 100

		# recenter grid on best (A=AIC, B=BIC) ' ' if no recenter
		self.recenter = 'B'
		# grid expansion factor (1 if no expansion)
		self.expandby = 0.5

		self.agn = 'AGN'
		self.list = self.agn+'.lis'

		lis = open(self.workdir+self.list,'a')
		lis.write('# filter scope datafile\n')
		lis.close()

		if clean_input:
			os.system('rm '+self.workdir+self.list)
		self.df2 = {}
		self.ctr = 0
		self.band = 'X'

		self.input_lcs = {}

	def run(self):
		self.lc_names = self.input_lcs.Tel.unique()
		self.make_param_file()
		#print(self.workdir+'./dream '+self.param_file)
		os.system('cp '+self.module_path+self.exec_file+' '+self.workdir+'/.')
		os.chdir(self.workdir)
		#print(os.pwd())
		os.system('./dream.sh')
		os.chdir('..')
		#   Col 1 : HJD
		#   Col 2 : flux
		#   Col 3 : rms statistical error
		#   Col 4 : rms systematic error
		#   Col 5 : scope (see key below)
		#   Col 6 : add
		#   Col 7 : scl

		#self.read_out(self.workdir+self.agn+'_'+self.band+'_dream.dat')


	def add_lc(self,telescope,data):

		lc_name = self.band+'_'+telescope+'.dat'
		pf = open(self.workdir+lc_name,'w')
		lis = open(self.workdir+self.list,'a')
		lis.write(self.band+' '+telescope+' '+lc_name+'\n')
		lis.close()
		ndata = data.shape[0]
		for i in range(ndata):
			pf.write("{:12.6f} {:8.3f} {:8.3f}\n".format(data[i][0],data[i][1],data[i][2]))
			self.df2[self.ctr] = {'MJD': data[i][0], 
					'Flux': data[i][1],
					'Error': data[i][2],
					'Tel': telescope,
					}

			self.ctr += 1
		pf.close()

		self.input_lcs = pd.DataFrame.from_dict(self.df2,"index")

	def read_out(self,location):
		self.ouptput_lcs = pd.read_csv(location,
				delim_whitespace=True,
				names=['MJD','Flux','Error_stat',
						'Error_sys','tel','add','scl'])

	def make_param_file(self):

		pf = open(self.workdir+'dream.sh','w')

		pf.write("# shell script runs dream on F9 B data\n")
		pf.write("# 2020 Jun Keith Horne @ St Andrews\n")
		pf.write("\n")
		#pf.write("set dt = {}\n".format(self.dt))
		#pf.write("set roa = {}\n".format(self.roa))
		#pf.write("set hw = {}\n".format(self.hw))
		#pf.write("\n")
		#pf.write("set nits = {}\n".format(self.nits))
		#pf.write("\n")
		#pf.write("set agn = {}\n".format(self.agn))
		#pf.write("\n")
		#pf.write("set infile = {}\n".format(self.list))
		#pf.write("set plotx = $agn'_dream_x.ps'\n")
		#pf.write("set plotlc = $agn'_dream_lc.ps'\n")
		pf.write("\n")
		pf.write("date\n")
		pf.write("./dream.exe << $\n")
		pf.write("\n")
		pf.write("d\n")
		pf.write("{}\n".format(self.list))
		pf.write("{}\n".format(self.dt))
		pf.write("{}\n".format(self.roa))
		pf.write("{}\n".format(self.hw))
		pf.write("\n")
		pf.write("g\n")
		pf.write("h\n")
		pf.write("{} {}\n".format(self.grid1,self.grid2))
		pf.write("{}\ni\n{}\n".format(self.ngrid,self.nits1))
		pf.write("\n")
		pf.write("p\n")
		pf.write("c\n")
		pf.write("{}\n".format(self.agn+'_dream_grid1.ps'))
		pf.write("u\n")
		pf.write("p\n")
		pf.write("n\n")
		pf.write("n\n")
		pf.write("{}\n".format(self.recenter))
		pf.write("x\n")
		pf.write("{}\n".format(self.expandby))
		pf.write("i\n")
		pf.write("{}\n".format(self.nits2))
		pf.write("p\n")
		pf.write("c\n")
		pf.write("{}\n".format(self.agn+'_dream_grid2.ps'))
		pf.write("u\n")
		pf.write("p\n")
		pf.write("n\n")
		pf.write("n\n")
		pf.write("q\n")

		pf.write("i\n")
		pf.write("{}\n".format(self.nits))
		pf.write("\n")
		pf.write("	! convergence plot\n")
		pf.write("x\n")
		pf.write("c\n")
		pf.write("{}\n".format(self.agn+'_dream_x.ps'))
		pf.write("u\n")
		pf.write("p\n")
		pf.write("n\n")
		pf.write("n\n")
		pf.write("\n")
		pf.write("	! lightcurve plot\n")
		pf.write("l\n")
		pf.write("c\n")
		pf.write("{}\n".format(self.agn+'_dream_lc.ps'))
		pf.write("u\n")
		pf.write("p\n")
		pf.write("n\n")
		pf.write("n\n")
		pf.write("\n")
		pf.write("	! output\n")
		pf.write("o\n")
		pf.write("{}\n".format(self.agn))
		pf.write("\n")
		pf.write("\n")
		pf.write("q\n")
		pf.write("\n")
		pf.write("$\n")
		pf.write("date\n")
		pf.close()
		os.system('chmod 777 '+self.workdir+'dream.sh')
