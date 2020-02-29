#! /usr/bin/env python
#-*- coding: UTF-8 -*-


'''Módulo para implementar grillas hexagonales. Se definen la grilla
propiamente y las celdas, paredes y vértices que la componen. 
Ademas cada objeto puede calcular las relaciones existentes con los
otros objetos de la grilla, como vecindad, adyacencia, etc.
Este módulo solo define y gestiona estos objetos, pero no toma partido
en cuanto a dimensiones ni propiedades gráficas. Para poder dibujar
una grilla se debe extender estos objetos agregando las propiedades 
que definen las dimensiones y los métodos y funciones que permitan 
graficarla


Autor: Martín S. López Paglione
e-mail: martincholp@hotmail.com
'''
class Grilla(object):
	"""Grilla de celdas hexagonales"""
	def __init__(self, filas, columnas):
		'''Grilla de celdas hexagonales (tipo panal de abejas)
		Los parámetros filas y columnas me dan la dimensión de la 
		grilla. 
		La forma de las celdas serán hexágonos horizontales, y las 
		columnas impares estarán más bajas que las pares.'''
		self._filas = filas
		self._columnas = columnas

		self._celdas = {}  #  (f, c)
		self._paredes = {}  #  ((f, c), "NO|N|NE")
		self._vertices = {}  #  ((f, c), "O|E")

		# Para crear la grilla debemos ir creando cada elemento
		# individualmente y almacenarlos en la posición que
		# corresponde

		for f in xrange(0, filas):
			for c in xrange(0, columnas):

				# Verifico que la celda no exista
				if not (f, c) in self._celdas: 

					# Creo la celda
					new_celda = _Celda((f, c))

					# La vinculo a la grilla padre
					new_celda._Celda__grid = self  
												  
					# Agrego la celda al diccionario
					self._celdas[(f, c)] = new_celda


					# Creo las paredes
					# Las paredes pueden depender de si la columna es
					# par o impar

					# Indice de las paredes
					if not c%2:  # Si es par 
						# NO
						pos_pared_NO = ((f, c), "NO")

						# N 
						pos_pared_N = ((f, c), "N")

						# NE
						pos_pared_NE = ((f, c), "NE")

						# SE
						pos_pared_SE = ((f,c+1), "NO")

						# S
						pos_pared_S = ((f+1,c), "N")

						# SO
						pos_pared_SO = ((f,c-1), "NE")

					else:  # Si es impar
						# NO
						pos_pared_NO = ((f, c), "NO")

						# N 
						pos_pared_N = ((f, c), "N")

						# NE
						pos_pared_NE = ((f, c), "NE")

						# SE
						pos_pared_SE = ((f+1,c+1), "NO")

						# S
						pos_pared_S = ((f+1,c), "N")

						# SO
						pos_pared_SO = ((f+1,c-1), "NE")

					pos_paredes = (pos_pared_NO, pos_pared_N, pos_pared_NE, pos_pared_SE, pos_pared_S, pos_pared_SO)

					for cur_pos_pared in pos_paredes:

						# Verifico si existe o no cada pared
						if not cur_pos_pared in self._paredes:

							# Creo la pared
							new_pared = _Pared(cur_pos_pared)

							# La vinculo a la grilla padre
							new_pared._Pared__grid = self  
														  
							# Agrego la pared al diccionario
							self._paredes[cur_pos_pared] = new_pared


					# Creo los vértices
					# Los vértices pueden depender de si la columna es
					# par o impar

					# Indice de los vértices
					if not c%2:  # Si es par 
						# NO
						pos_vertice_NO = ((f-1, c-1), "E")

						# NE
						pos_vertice_NE = ((f-1, c+1), "O")

						# E
						pos_vertice_E = ((f, c), "E")

						# SE
						pos_vertice_SE = ((f, c+1), "O")

						# SO
						pos_vertice_SO = ((f, c-1), "E")

						# O
						pos_vertice_O = ((f, c), "O")

					else:  # Si es impar
						# NO
						pos_vertice_NO = ((f, c-1), "E")

						# NE
						pos_vertice_NE = ((f, c+1), "O")

						# E
						pos_vertice_E = ((f, c), "E")

						# SE
						pos_vertice_SE = ((f+1, c+1), "O")

						# SO
						pos_vertice_SO = ((f+1, c-1), "E")

						# O
						pos_vertice_O = ((f, c), "O")


					pos_vertices = (pos_vertice_NO, pos_vertice_NE, pos_vertice_E, pos_vertice_SE, pos_vertice_SO, pos_vertice_O)

					for cur_pos_vertice in pos_vertices:

						# Verifico si existe o no cada vértice
						if not cur_pos_vertice in self._vertices:

							# Creo el vértice
							new_vertice = _Vertice(cur_pos_vertice)

							# Lo vinculo a la grilla padre
							new_vertice._Vertice__grid = self  
														  
							# Agrego el vértice al diccionario
							self._vertices[cur_pos_vertice] = new_vertice

	@property
	def cant_filas(self):
		'''Cantidad de filas de la grilla. Solo lectura.'''
		return self._filas

	@property
	def cant_columnas(self):
		'''Cantidad de columnas de la grilla. Solo lectura.'''
		return self._columnas

	@property
	def cant_celdas(self):
		'''Cantidad de celdas de la grilla. Solo lectura.'''
		return len(self._celdas)

	@property
	def cant_paredes(self):
		'''Cantidad de paredes de la grilla. Solo lectura.'''
		return len(self._paredes)

	@property
	def cant_vertices(self):
		'''Cantidad de vértices de la grilla. Solo lectura.'''
		return len(self._vertices)

	def __str__(self):
		msg = "Grilla hexagonal de " + str(self.cant_filas) + " filas y " + str(self.cant_columnas) + " columnas"
		return msg

	def __repr__(self):
		msg = "Grilla hexagonal de " + str(self.cant_filas) + " filas y " + str(self.cant_columnas) + " columnas"
		return msg

	def __getitem__(self, pos):
		'''Retorna la celda indicada en pos'''
		return self._celdas[pos]

	def __len__(self):
		'''Cantidad de celdas de la grilla'''
		return self.cant_celdas()

	def get_celda(self, pos):
		'''Retorna la celda indicada en pos'''
		return self._celdas[pos]

	def get_pared(self, pos):
		'''Retorna la pared indicada en pos'''
		return self._paredes[pos]
		
	def get_vertice(self, pos):
		'''Retorna el vertice indicado en pos'''
		return self._vertices[pos]
		
	def get_columna(self, numCol):
		'''Retorna una lista con las celdas que pertenecen a la 
		columna numCol, ordenadas por fila'''
		col = [celda for celda in self._celdas.values() if celda.columna == numCol]
		col.sort(key= lambda c:c.fila)
		return col

	def get_fila(self, numFil):
		'''Retorna una lista con las celdas que pertenecen a la fila
		numFil, ordenadas por columna'''
		fil = [celda for celda in self._celdas.values() if celda.fila == numFil]
		fil.sort(key= lambda c:c.columna)
		return fil	

	def index_celdas(self):
		'''Retorna una lista con todos los indices de las celdas de 
		la grilla'''
		return self._celdas.keys()

	def index_paredes(self):
		'''Retorna una lista con todos los indices de las paredes de 
		la grilla'''
		return self._paredes.keys()
		
	def index_vertices(self):
		'''Retorna una lista con todos los indices de los vértices de 
		la grilla'''
		return self._vertices.keys()

class _Celda(object):
	"""Celda hexagonal"""
	def __init__(self, pos):
		'''Define una celda hexagonal. El parámetro pos es una
		tupla que indica la fila y columna de la celda.'''

		self._pos = pos  # Coordenadas en la grilla
		self.__grid = None  # Grilla a la que pertenece

	@property
	def grilla(self):
		'''Devuelve la grilla a la que pertenece la celda'''
		return self.__grid
		
	@property
	def posicion(self):
		'''Devuelve las coordenadas de la celda. Solo lectura'''
		return self._pos
	
	@property
	def fila(self):
		'''Devuelve la fila de la celda. Solo lectura'''
		return self._pos[0]
	
	@property
	def columna(self):
		'''Devuelve la columna de la celda. Solo lectura'''
		return self._pos[1]

	def __str__(self):
		msg = "Celda " + str(self.posicion)
		return msg

	def __repr__(self):
		msg = "Celda " + str(self.posicion)
		return msg
	
	def paredes(self):
		'''Devuelve un diccionario con las paredes de la celda. La 
		clave del diccionario es la posición relativa, y el valor la 
		pared en cuestión. La posición relativa es un string que puede 
		tomar cualquiera de los siguientes valores:
		
		"N"  --> pared norte
		"NE" --> pared noreste
		"SE" --> pared sudeste
		"S"  --> pared sur
		"SO" --> pared sudoeste
		"NO" --> pared noroeste

		Para obtener solo una de las paredes se puede emplear el 
		siguiente código:

		>>> pared_Norte = objCelda.paredes()["N"]'''

		# Fila y columna de la celda actual
		f, c = self._pos

		# Las paredes se extraen del conjunto de paredes de la grilla
		# padre, y su índice depende de si la columna es par o impar
		
		# Indice de las paredes
		if not c%2:  # Si es par 
			# NO
			pos_pared_NO = ((f, c), "NO")

			# N 
			pos_pared_N = ((f, c), "N")

			# NE
			pos_pared_NE = ((f, c), "NE")

			# SE
			pos_pared_SE = ((f,c+1), "NO")

			# S
			pos_pared_S = ((f+1,c), "N")

			# SO
			pos_pared_SO = ((f,c-1), "NE")

		else:  # Si es impar
			# NO
			pos_pared_NO = ((f, c), "NO")

			# N 
			pos_pared_N = ((f, c), "N")

			# NE
			pos_pared_NE = ((f, c), "NE")

			# SE
			pos_pared_SE = ((f+1,c+1), "NO")

			# S
			pos_pared_S = ((f+1,c), "N")

			# SO
			pos_pared_SO = ((f+1,c-1), "NE")

		pos_paredes = (pos_pared_NO, pos_pared_N, pos_pared_NE, pos_pared_SE, pos_pared_S, pos_pared_SO)
		posRel = ("NO", "N", "NE", "SE", "S", "SO")

		res_paredes = {}
		for k in xrange(0,6):
			res_paredes[posRel[k]] = self.__grid.get_pared(pos_paredes[k])

		return res_paredes

	def get_pared(self, posRel):
		'''Devuelve la pared indicada en posRel. posRel es la posición 
		de la pared relativa a la celda, y es un string que puede 
		tomar cualquiera de los siguientes valores:
		
		"N"  --> pared norte
		"NE" --> pared noreste
		"SE" --> pared sudeste
		"S"  --> pared sur
		"SO" --> pared sudoeste
		"NO" --> pared noroeste'''

		return self.paredes()[posRel]
		
	def vecinas(self):
		'''Devuelve un diccionario con las celdas vecinas. La clave
		del diccionario es la posición relativa, y el valor la celda 
		vecina en cuestión.
		La posición relativa es un string que puede tomar cualquiera 
		de los siguientes valores:
		
		"N"  --> vecina norte
		"NE" --> vecina noreste
		"SE" --> vecina sudeste
		"S"  --> vecina sur
		"SO" --> vecina sudoeste
		"NO" --> vecina noroeste'''


		# Fila y columna de la celda actual
		f, c = self._pos

		# Las celdas vecinas se extraen del conjunto de celdas de la 
		# grilla padre, y su índice depende de si la columna es par o
		# impar
		
		# Índice de las vecinas
		if not c%2:  # Si es par 
			# NO
			pos_vecina_NO = (f-1, c-1)

			# N 
			pos_vecina_N = (f-1, c)

			# NE
			pos_vecina_NE = (f-1, c+1)

			# SE
			pos_vecina_SE = (f,c+1)

			# S
			pos_vecina_S = (f+1,c)

			# SO
			pos_vecina_SO = (f,c-1)

		else:  # Si es impar
			# NO
			pos_vecina_NO = (f, c-1)

			# N 
			pos_vecina_N = (f-1, c)

			# NE
			pos_vecina_NE = (f, c+1)

			# SE
			pos_vecina_SE = (f+1,c+1)

			# S
			pos_vecina_S = (f+1,c)

			# SO
			pos_vecina_SO = (f+1,c-1)

		pos_vecinas = (pos_vecina_NO, pos_vecina_N, pos_vecina_NE, pos_vecina_SE, pos_vecina_S, pos_vecina_SO)
		posRel = ("NO", "N", "NE", "SE", "S", "SO")

		res_vecinas = {}
		indice_celdas = self.__grid.index_celdas()
		for k in xrange(0,6):
			if pos_vecinas[k] in indice_celdas:  # Verifico que la celda exista
				res_vecinas[posRel[k]] = self.__grid.get_celda(pos_vecinas[k])
			else:  # Si no existe entonces es un borde y no hay vecina
				res_vecinas[posRel[k]] = None

		return res_vecinas

	def get_vecina(self, posRel):
		'''Devuelve la vecina indicada en posRel. posRel es la 
		posición de la vecina relativa a la celda, y es un string que 
		puede tomar cualquiera de los siguientes valores:
		
		"N"  --> vecina norte
		"NE" --> vecina noreste
		"SE" --> vecina sudeste
		"S"  --> vecina sur
		"SO" --> vecina sudoeste
		"NO" --> vecina noroeste'''
		
		return self.vecinas()[posRel]

	def vertices(self):
		'''Devuelve un diccionario con los vértices de la celda. 
		La clave del diccionario es la posición relativa, y el valor 
		el vértice en cuestión.
		La posición relativa es un string que puede tomar cualquiera 
		de los siguientes valores:
		
		"NE" --> vértice noreste
		"E"  --> vértice este
		"SE" --> vértice sudeste
		"SO" --> vértice sudoeste
		"O"  --> vértice oeste
		"NO" --> vértice noroeste'''

		# Fila y columna de la celda actual
		f, c = self._pos

		# Los vértices se extraen del conjunto de vértices de la 
		# grilla padre, y su índice depende de si la columna es par o
		# impar
		
		# Índice de los vértices
		if not c%2:  # Si es par 
			# NO
			pos_vertice_NO = ((f-1, c-1), "E")

			# NE
			pos_vertice_NE = ((f-1, c+1), "O")

			# E
			pos_vertice_E = ((f, c), "E")

			# SE
			pos_vertice_SE = ((f, c+1), "O")

			# SO
			pos_vertice_SO = ((f, c-1), "E")

			# O
			pos_vertice_O = ((f, c), "O")

		else:  # Si es impar
			# NO
			pos_vertice_NO = ((f, c-1), "E")

			# NE 
			pos_vertice_NE = ((f, c+1), "O")

			# E
			pos_vertice_E = ((f, c), "E")

			# SE
			pos_vertice_SE = ((f+1, c+1), "O")

			# SO
			pos_vertice_SO = ((f+1, c-1), "E")

			# O
			pos_vertice_O = ((f, c), "O")

		pos_vertices = (pos_vertice_NO, pos_vertice_NE, pos_vertice_E, pos_vertice_SE, pos_vertice_SO, pos_vertice_O)
		posRel = ("NO", "NE", "E", "SE", "SO", "O")

		res_vertices = {}
		
		for k in xrange(0,6):
			res_vertices[posRel[k]] = self.__grid.get_vertice(pos_vertices[k])

		return res_vertices

	def get_vertice(self, posRel):
		'''Devuelve el vértice indicado en posRel. posRel es la 
		posición de la vecina relativa a la celda, y es un string que 
		puede tomar cualquiera de los siguientes valores:
		
		"NE" --> vertice noreste
		"E"  --> vertice este
		"SE" --> vertice sudeste
		"SO" --> vertice sudoeste
		"O"  --> vertice oeste
		"NO" --> vertice noroeste'''

		return self.vertices()[posRel]
	
class _Pared(object):
	"""Pared de la celda. El parámetro pos es una tupla	que indica la
	posición de la pared. Para identificar una posición	se debe pasar
	la posición de la celda que está debajo de la pared	en el primer
	elemento, y la posición relativa de la pared en el segundo 
	elemento. Para las paredes que no pueden nombrarse de esta forma 
	por tener solo una celda adyacente, y que no se corresponde con la
	nomenclatura, se nombrará de igual forma, suponiendo que la celda 
	en cuestión si existe. Aunque no estará físicamente en la grilla, 
	es decir que no forma parte de ésta, será una celda fantasma y 
	servirá solamente para poder nombrar la pared. 
	Las posiciones relativas de una pared respecto a una celda a la
	que pertenece se nombran con puntos cardinales. N para la pared
	superior, NE para la superior derecha, SE para la inferior
	derecha, etc. Notar que una pared se puede identificar de varias
	formas, por ejemplo la pared S de la celda (f, c), donde f es la
	fila y c la columna, es también la pared N de la celda (f+1, c).
	Sin embargo, al momento de definir la pared se usará la forma
	indicada mas arriba.
	Un ejemplo de celda fantasma sería aquella que define una pared
	del borde inferior. Si nuestra grilla tiene f filas, la pared S de
	la celda (f, c) tendría la posición ((f+1, c), N) aunque la celda
	que menciona no existe. En el caso de la pared SO de una celda de 
	la columna 0, la pared sería nombrada referida a una columna con
	índice negativo."""
	def __init__(self, pos):

		self._pos = pos
		self.__grid = None  # Grilla a la que pertenece

	@property
	def grilla(self):
		'''Devuelve la grilla a la que pertenece la pared'''
		return self.__grid

	@property
	def id(self):
		'''Devuelve la posición que identifica a la pared. Solo 
		lectura'''
		return self._pos

	def __str__(self):
		msg = "Pared " + str(self.id)
		return msg

	def __repr__(self):
		msg = "Pared " + str(self.id)
		return msg

	def vertices(self):
		'''Devuelve un diccionario con los vértices de la pared. 
		La clave del diccionario es la posición relativa, y el valor 
		el vértice en cuestión. '''
		
		# Cada pared tiene 2 vértices, y obtenerlos depende de si la
		# columna de su id es par o impar, y de la posición relativa
		# en su id

		f, c = self.id[0]  # fila y columna del id de la pared
		p = self.id[1]  # posición reltiva del id de la pared

		if p == "NO":
			if not c%2:
				pos_A = ((f  , c  ), "O")
				pos_B = ((f-1, c-1), "E")
			else:
				pos_A = ((f  , c  ), "O")
				pos_B = ((f  , c-1), "E")

		elif p == "N":
			if not c%2:
				pos_A = ((f-1, c-1), "E")
				pos_B = ((f-1, c+1), "O")
			else:
				pos_A = ((f  , c-1), "E")
				pos_B = ((f  , c+1), "O")

		elif p == "NE":
			if not c%2:
				pos_A = ((f-1, c+1), "O")
				pos_B = ((f  , c  ), "E")
			else:
				pos_A = ((f  , c+1), "O")
				pos_B = ((f  , c  ), "E")

		res_vertices = {"A":self.__grid.get_vertice(pos_A), "B":self.__grid.get_vertice(pos_B) }

		return res_vertices

	def get_vertice(self, posRel):
		'''Devuelve el vértice indicado en posRel. posRel es la 
		posición del vertice relativo a la pared, y es un string que 
		puede tomar cualquiera de los siguientes valores:
		
		"A" --> Es el vértice inicial
		"B" --> Es el vértice final

		El vértice inicial (o vértice A) es el que tiene la coordenada
		horizontal de menor valor, es decir que se encuentra mas a la 
		izquierda. El otro vértice se considera vértice final (o 
		vértice B)'''

		return self.vertices()[posRel]

	def celdas(self):
		'''Devuelve un diccionario con las celdas adyacentes. La clave
		del diccionario es la posición relativa, y el valor la celda 
		adyacente en cuestión. Si el valor de celda es None entonces
		la pared es un borde.'''

		# Cada pared tiene 2 celdas adyacentes, y obtenerlas depende 
		# de si la columna de su id es par o impar, y de la posición 
		# relativa en su id

		f, c = self.id[0]  # fila y columna del id de la pared
		p = self.id[1]  # posición reltiva del id de la pared

		if p == "NO":
			if not c%2:
				pos_A = (f-1 , c-1)
				pos_B = (f   , c  )
			else:
				pos_A = (f  , c-1)
				pos_B = (f  , c  )

		elif p == "N":  # no importa si c es par o impar, pero se
						# mantiene esa misma lógica por consistencia
			if not c%2:
				pos_A = (f-1, c)
				pos_B = (f  , c)
			else:
				pos_A = (f-1, c)
				pos_B = (f  , c)

		elif p == "NE":
			if not c%2:
				pos_A = (f-1, c+1)
				pos_B = (f  , c  )
			else:
				pos_A = (f  , c+1)
				pos_B = (f  , c  )

		indice_celdas = self.__grid.index_celdas()
		res_celdas = {}
		if pos_A in indice_celdas:  # Verifico que la celda exista
			res_celdas['A'] = self.__grid.get_celda(pos_A)
		else:  # Si no existe entonces es un borde
			res_celdas['A'] = None

		if pos_B in indice_celdas:  # Verifico que la celda exista
			res_celdas['B'] = self.__grid.get_celda(pos_B)
		else:  # Si no existe entonces es un borde
			res_celdas['B'] = None

		return res_celdas

	def get_celda(self, posRel):
		'''Devuelve la celda adyacente indicada en posRel. posRel es 
		la posición de la celda relativo a la pared, y es un string 
		que puede tomar cualquiera de los siguientes valores:
		
		"A" --> Es la celda superior
		"B" --> Es la celda inferior

		La celda superior (o celda A) es la que tiene la coordenada
		vertical de menor valor, es decir la que se encuentra por 
		encima de la pared. La otra celda se considera celda inferior 
		(o celda B)''' 

		return self.celdas()[posRel]
	
	def continuaciones(self):
		'''Devuelve un diccionario con las paredes con las que 
		comparte un vértice. La clave del diccionario es la posición
		relativa, y el valor la pared en cuestion'''

		# Cada pared tiene 4 paredes continuaciones, y obtenerlas 
		# depende de si la columna de su id es par o impar, y de la 
		# posición relativa en su id

		f, c = self.id[0]  # fila y columna del id de la pared
		p = self.id[1]  # posición reltiva del id de la pared

		if p == "NO":
			if not c%2:
				pos_AI = ((f  , c-1), "NE")
				pos_AD = ((f  , c-1), "N")
				pos_BI = ((f-1, c-1), "NE")
				pos_BD = ((f  , c  ), "N")
			else:
				pos_AI = ((f+1, c-1), "NE")
				pos_AD = ((f+1, c-1), "N")
				pos_BI = ((f  , c-1), "NE")
				pos_BD = ((f  , c  ), "N")

		elif p == "N":  

			if not c%2:
				pos_AI = ((f  , c  ), "NO")
				pos_AD = ((f-1, c-1), "NE")
				pos_BI = ((f-1, c+1), "NO")
				pos_BD = ((f  , c  ), "NE")
			else:
				pos_AI = ((f  , c  ), "NO")
				pos_AD = ((f  , c-1), "NE")
				pos_BI = ((f  , c+1), "NO")
				pos_BD = ((f  , c  ), "NE")

		elif p == "NE":
			if not c%2:
				pos_AI = ((f  , c  ), "N")
				pos_AD = ((f-1, c+1), "NO")
				pos_BI = ((f  , c+1), "N")
				pos_BD = ((f  , c+1), "NO")
			else:
				pos_AI = ((f  , c  ), "N")
				pos_AD = ((f  , c+1), "NO")
				pos_BI = ((f+1, c+1), "N")
				pos_BD = ((f+1, c+1), "NO")

		res_continuaciones = {} 
		indice_paredes = self.__grid.index_paredes()

		if pos_AI in indice_paredes:  # Verifico que la celda exista
			res_continuaciones["AI"] = self.__grid.get_pared(pos_AI)
		else:  # Si no existe entonces es un borde y no hay vecina
			res_continuaciones["AI"] = None

		if pos_AD in indice_paredes:  # Verifico que la celda exista
			res_continuaciones["AD"] = self.__grid.get_pared(pos_AD)
		else:  # Si no existe entonces es un borde y no hay vecina
			res_continuaciones["AD"] = None
		
		if pos_BI in indice_paredes:  # Verifico que la celda exista
			res_continuaciones["BI"] = self.__grid.get_pared(pos_BI)
		else:  # Si no existe entonces es un borde y no hay vecina
			res_continuaciones["BI"] = None
		
		if pos_BD in indice_paredes:  # Verifico que la celda exista
			res_continuaciones["BD"] = self.__grid.get_pared(pos_BD)
		else:  # Si no existe entonces es un borde y no hay vecina
			res_continuaciones["BD"] = None

		return res_continuaciones

	def get_continuacion(self, posRel):
		'''Devuelve la pared continuación indicada en posRel. posRel
		es la posición relativa de la pared continuación, y es un 
		string que puede tomar cualquiera de los siguientes valores:

		"AI"  --> Es la continuación izquierda del vértice A
		"AD"  --> Es la continuación derecha del vértice A
		"BI"  --> Es la continuación izquierda del vértice B
		"BD"  --> Es la continuación derecha del vértice B

		Para definir si es continuación izquierda o derecha nos 
		posicionamos sobre el vértice, dejando la pared a nuestras
		espaldas. Delante nuestro tendremos las continuaciones
		izquierda y derecha'''


		return self.continuaciones()[posRel]

class _Vertice(object):
	"""Vértice de una celda. El parámetro pos es una tupla que define
	la posición del vértice. Para identificar la posición se debe 
	pasar la posición de la celda y la posición relativa del vértice.
	La posición relativa será E u O, según corresponda, ya que los 
	otros vértices podrán nombrarse relativos a otra celda siguiendo 
	esta misma regla. En caso de que el vértice no se pueda nombrar 
	porque la celda a la que pertenecería no existe, se procede igual
	que en el caso de las paredes, suponiendo una celda fantasma y 
	nombrando al vértice relativo a ésta. Ésta celda fantasma 
	realmente no existe y sirve solamente para nombrar el vértice. """
	def __init__(self, pos):
		
		self._pos = pos
		self.__grid = None  # Grilla a la que pertenece

	@property
	def grilla(self):
		'''Devuelve la grilla a la que pertenece el vértice'''
		return self.__grid
		
	@property
	def id(self):
		'''Devuelve la posicion que identifica al vértice. Solo 
		lectura'''
		return self._pos

	def __str__(self):
		msg = "Vertice " + str(self.id)
		return msg
	
	def __repr__(self):
		msg = "Vertice " + str(self.id)
		return msg
	
	def paredes(self):
		'''Devuelve un diccionario con las paredes que convergen en el
		vértice. La clave del diccionario es la posición relativa, y 
		el valor la pared en cuestión'''

		f, c = self.id[0]  # fila y columna del id del vertice
		p = self.id[1]  # posición reltiva del id del vertice

		if p == "E":
			if not c%2:
				pos_A = ((f  , c  ), "NE")
				pos_B = ((f  , c+1), "N")
				pos_C = ((f  , c+1), "NO")
			else:
				pos_A = ((f  , c  ), "NE")
				pos_B = ((f+1, c+1), "N")
				pos_C = ((f+1, c+1), "NO")

		elif p == "O":
			if not c%2:
				pos_A = ((f  , c  ), "NO")
				pos_B = ((f  , c-1), "NE")
				pos_C = ((f  , c-1), "N")
			else:
				pos_A = ((f  , c  ), "NO")
				pos_B = ((f+1, c-1), "NE")
				pos_C = ((f+1, c-1), "N")



		indice_paredes = self.__grid.index_paredes()
		res_paredes = {}
		if pos_A in indice_paredes:  # Verifico que la pared exista
			res_paredes['A'] = self.__grid.get_pared(pos_A)
		else:  # Si no existe entonces es un borde
			res_paredes['A'] = None

		if pos_B in indice_paredes:  # Verifico que la pared exista
			res_paredes['B'] = self.__grid.get_pared(pos_B)
		else:  # Si no existe entonces es un borde
			res_paredes['B'] = None

		if pos_C in indice_paredes:  # Verifico que la pared exista
			res_paredes['C'] = self.__grid.get_pared(pos_C)
		else:  # Si no existe entonces es un borde
			res_paredes['C'] = None

		return res_paredes

	def get_pared(self, posRel):
		'''Devuelve la pared indicada en posRel. posRel es la posición 
		de la pared relativa al vértice, y es un string que puede 
		tomar cualquiera de los siguientes valores:
		
		"A" --> primera pared
		"B" --> segunda pared
		"C" --> tercera pared

		La primera pared (o pared A), es aquella que en su 
		identificador tiene la misma coordenada de celda que la que 
		tiene el vértice. Numerando las paredes restantes en el 
		sentido de giro de las agujas de un reloj obtenemos la segunda
		y tercer pared (o paredes B y C respectivamente). Notar que
		si el vértice se encuentra en un borde, alguna de las paredes 
		adyacentes será None, indicando que pertenece a una celda 
		fantasma'''

		return self.paredes()[posRel]

	def celdas(self):
		'''Devuelve un diccionario con las celdas adyacentes. La clave
		del diccionario es la posición relativa, y el valor la celda 
		adyacente en cuestión'''

		f, c = self.id[0]  # fila y columna del id del vertice
		p = self.id[1]  # posición reltiva del id del vertice

		if p == "E":
			if not c%2:
				pos_A = (f  , c  )
				pos_B = (f-1, c+1)
				pos_C = (f  , c+1)
			else:
				pos_A = (f  , c  )
				pos_B = (f  , c+1)
				pos_C = (f+1, c+1)

		elif p == "O":
			if not c%2:
				pos_A = (f  , c  )
				pos_B = (f  , c-1)
				pos_C = (f-1, c-1)
			else:
				pos_A = (f  , c  )
				pos_B = (f+1, c-1)
				pos_C = (f  , c-1)



		indice_celdas = self.__grid.index_celdas()
		res_celdas = {}

		if pos_A in indice_celdas:  # Verifico que la celda exista
			res_celdas['A'] = self.__grid.get_celda(pos_A)
		else:  # Si no existe entonces es un borde
			res_celdas['A'] = None

		if pos_B in indice_celdas:  # Verifico que la celda exista
			res_celdas['B'] = self.__grid.get_celda(pos_B)
		else:  # Si no existe entonces es un borde
			res_celdas['B'] = None

		if pos_C in indice_celdas:  # Verifico que la celda exista
			res_celdas['C'] = self.__grid.get_celda(pos_C)
		else:  # Si no existe entonces es un borde
			res_celdas['C'] = None

		return res_celdas
	
	def get_celda(self, posRel):
		'''Devuelve la celda adyacente indicada en posRel. posRel es 
		la posición de la celda relativo al vertice, y es un string 
		que puede tomar cualquiera de los siguientes valores:
		
		"A" --> Primera celda
		"B" --> Segunda celda
		"C" --> Tercera celda

		La primera celda (o celda A), es aquella que en su 
		identificador tiene la misma coordenada de celda que la que 
		tiene el vértice. Numerando las celdas restantes en el sentido
		de giro de las agujas de un reloj obtenemos la segunda y 
		tercer celda (o celdas B y C respectivamente). Notar que si el
		vértice se encuentra en un borde, alguna de las celdas 
		adyacentes será None, indicando que ésta es una celda fantasma'''

		return self.celdas()[posRel]

