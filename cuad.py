#! /usr/bin/env python
#-*- coding: UTF-8 -*-


'''Módulo para implementar grillas cuadradas. Se definen la grilla
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
	"""Grilla de celdas cuadradas"""
	def __init__(self, filas, columnas):
		'''Grilla de celdas cuadradas 
		Los parámetros filas y columnas me dan la dimensión de la 
		grilla. 
		'''
		self._filas = filas
		self._columnas = columnas

		self._celdas = {}  #  (f, c)
		self._paredes = {}  #  ((f, c), "N|O")
		self._vertices = {}  #  (f, c)

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

					# Indice de las paredes
					# N
					pos_pared_N = ((f, c), "N")

					# E 
					pos_pared_E = ((f, c+1), "O")

					# S
					pos_pared_S = ((f+1, c), "N")

					# O
					pos_pared_O = ((f,c), "O")


					pos_paredes = (pos_pared_N, pos_pared_E, pos_pared_S, pos_pared_O)

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

					# Indice de los vértices
					
					# NO
					pos_vertice_NO = (f, c)

					# NE
					pos_vertice_NE = (f, c+1)

					# SE
					pos_vertice_SE = (f+1, c+1)

					# SO
					pos_vertice_SO = (f+1, c)


					pos_vertices = (pos_vertice_NO, pos_vertice_NE, pos_vertice_SE, pos_vertice_SO)

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
		msg = "Grilla cuadrada de " + str(self.cant_filas) + " filas y " + str(self.cant_columnas) + " columnas"
		return msg

	def __repr__(self):
		msg = "Grilla cuadrada de " + str(self.cant_filas) + " filas y " + str(self.cant_columnas) + " columnas"
		return msg

	def __getitem__(self, pos):
		'''Retorna la celda indicada en fila,columna'''
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
	"""Celda cuadrada"""
	def __init__(self, pos):
		'''Define una celda cuadrada. El parámetro pos es una
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
		
		"N" --> pared norte
		"E" --> pared este
		"S" --> pared sur
		"O" --> pared oeste

		Para obtener solo una de las paredes se puede emplear el 
		siguiente código:

		>>> pared_Norte = objCelda.paredes()["N"]'''

		# Fila y columna de la celda actual
		f, c = self._pos

		# Las paredes se extraen del conjunto de paredes de la grilla
		# padre
		
		# Indice de las paredes
	
		# N
		pos_pared_N = ((f, c), "N")

		# E 
		pos_pared_E = ((f, c+1), "O")

		# S
		pos_pared_S = ((f+1, c), "N")

		# O
		pos_pared_O = ((f,c), "O")


		pos_paredes = (pos_pared_N, pos_pared_E, pos_pared_S, pos_pared_O)
		posRel = ("N", "E", "S", "O")

		res_paredes = {}
		for k in xrange(0,4):
			res_paredes[posRel[k]] = self.__grid.get_pared(pos_paredes[k])

		return res_paredes

	def get_pared(self, posRel):
		'''Devuelve la pared indicada en posRel. posRel es la posición 
		de la pared relativa a la celda, y es un string que puede 
		tomar cualquiera de los siguientes valores:
		
		"N"  --> pared norte
		"E"  --> pared este
		"S"  --> pared sur
		"O"  --> pared oeste'''

		return self.paredes()[posRel]
		
	def vecinas(self):
		'''Devuelve un diccionario con las celdas vecinas. La clave
		del diccionario es la posición relativa, y el valor la celda 
		vecina en cuestión.
		La posición relativa es un string que puede tomar cualquiera 
		de los siguientes valores:
		
		"N"  --> vecina norte
		"E"  --> vecina este
		"S"  --> vecina sur
		"O"  --> vecina oeste'''


		# Fila y columna de la celda actual
		f, c = self._pos

		# Las celdas vecinas se extraen del conjunto de celdas de la 
		# grilla padre.
		
		# Índice de las vecinas
		
		# N
		pos_vecina_N = (f-1, c)

		# E 
		pos_vecina_E = (f, c+1)

		# S
		pos_vecina_S = (f+1, c)

		# O
		pos_vecina_O = (f, c-1)


		pos_vecinas = (pos_vecina_N, pos_vecina_E, pos_vecina_S, pos_vecina_O)
		posRel = ("N", "E", "S", "O")

		res_vecinas = {}
		indice_celdas = self.__grid.index_celdas()
		for k in xrange(0,4):
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
		"E"  --> vecina este
		"S"  --> vecina sur
		"O"  --> vecina oeste'''
		
		return self.vecinas()[posRel]

	def vertices(self):
		'''Devuelve un diccionario con los vértices de la celda. 
		La clave del diccionario es la posición relativa, y el valor 
		el vértice en cuestión.
		La posición relativa es un string que puede tomar cualquiera 
		de los siguientes valores:
		
		"NO"  --> vertice norte
		"NE"  --> vertice este
		"SE"  --> vertice sur
		"SO"  --> vertice oeste'''

		# Fila y columna de la celda actual
		f, c = self._pos

		# Los vértices se extraen del conjunto de vértices de la 
		# grilla padre.
		
		# Índice de los vértices
		
		# NO
		pos_vertice_NO = (f, c)

		# NE 
		pos_vertice_NE = (f, c+1)

		# SE
		pos_vertice_SE = (f+1, c+1)

		# SO
		pos_vertice_SO = (f+1, c)

		pos_vertices = (pos_vertice_NO, pos_vertice_NE, pos_vertice_SE, pos_vertice_SO)
		posRel = ("NO", "NE", "SE", "SO")

		res_vertices = {}
		
		for k in xrange(0,4):
			res_vertices[posRel[k]] = self.__grid.get_vertice(pos_vertices[k])

		return res_vertices

	def get_vertice(self, posRel):
		'''Devuelve el vértice indicado en posRel. posRel es la 
		posición de la vecina relativa a la celda, y es un string que 
		puede tomar cualquiera de los siguientes valores:
		
		"NO"  --> vertice norte
		"NE"  --> vertice este
		"SE"  --> vertice sur
		"SO"  --> vertice oeste'''

		return self.vertices()[posRel]
	
class _Pared(object):
	"""Pared de la celda. El parámetro pos es una tupla	que indica la
	posición de la pared. Para identificar una posición	se debe pasar
	la posición de la celda que está debajo de la pared	o a su derecha
	según corresponda, y la posición relativa de la pared en el segundo 
	elemento. Para las paredes que no pueden nombrarse de esta forma 
	por tener solo una celda adyacente, y que no se corresponde con la
	nomenclatura, se nombrará de igual forma, suponiendo que la celda 
	en cuestión si existe. Aunque no estará físicamente en la grilla, 
	es decir que no forma parte de ésta, será una celda fantasma y 
	servirá solamente para poder nombrar la pared. 
	Las posiciones relativas de una pared respecto a una celda a la
	que pertenece se nombran con puntos cardinales. N para la pared
	superior, E para la derecha, S para la inferior y O para la 
	izquierda. Notar que una pared se puede identificar de varias
	formas, por ejemplo la pared S de la celda (f, c), donde f es la
	fila y c la columna, es también la pared N de la celda (f+1, c).
	Sin embargo, al momento de definir la pared se usará la forma
	indicada mas arriba.
	Un ejemplo de celda fantasma sería aquella que define una pared
	del borde inferior. Si nuestra grilla tiene f filas, la pared S de
	la celda (f, c) tendría la posición ((f+1, c), N) aunque la celda
	que menciona no existe. En el caso de la pared O de una celda de 
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
		el vértice en cuestión. La posición relativa es A para el
		vértice superior de una pared vertical, o si la pared es 
		horizontal es el vértice izquierdo. La posición B es el otro
		vértice (el inferior o el derecho, según sea el caso)'''
		
		# Cada pared tiene 2 vértices, y obtenerlos depende de la
		# posición relativa en su id

		f, c = self.id[0]  # fila y columna del id de la pared
		p = self.id[1]  # posición reltiva del id de la pared

		if p == "N":
			pos_A = (f  , c  )
			pos_B = (f  , c+1)

		elif p == "O":
			pos_A = (f  , c)
			pos_B = (f+1 , c)


		res_vertices = {"A":self.__grid.get_vertice(pos_A), "B":self.__grid.get_vertice(pos_B) }

		return res_vertices

	def get_vertice(self, posRel):
		'''Devuelve el vértice indicado en posRel. posRel es la 
		posición del vertice relativo a la pared, y es un string que 
		puede tomar cualquiera de los siguientes valores:
		
		"A" --> Es el vértice inicial
		"B" --> Es el vértice final

		El vértice inicial (o vértice A) es el superior si la pared es
		vertical o el izquierdo si es horizontal. El otro vértice se 
		considera vértice final (o vértice B)'''

		return self.vertices()[posRel]

	def celdas(self):
		'''Devuelve un diccionario con las celdas adyacentes. La clave
		del diccionario es la posición relativa, y el valor la celda 
		adyacente en cuestión. Si el valor de celda es None entonces
		la pared es un borde.'''

		# Cada pared tiene 2 celdas adyacentes, y obtenerlas depende 
		# de la posición relativa en su id.

		f, c = self.id[0]  # fila y columna del id de la pared
		p = self.id[1]  # posición reltiva del id de la pared

		if p == "N":
			pos_A = (f-1, c)
			pos_B = (f  , c)

		elif p == "O":  
			pos_A = (f  , c-1)
			pos_B = (f  , c)


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
		
		"A" --> Es la celda superior o izquierda
		"B" --> Es la celda inferior o derecha

		La celda A es la superior para una pared horizontal o la 
		izquierda para una pared vertical. La otra celda se 
		considera celda B''' 

		return self.celdas()[posRel]
	
	def continuaciones(self):
		'''Devuelve un diccionario con las paredes con las que 
		comparte un vértice. La clave del diccionario es la posición
		relativa, y el valor la pared en cuestion'''

		# Cada pared tiene 6 paredes continuaciones, y obtenerlas 
		# depende de la posición relativa en su id

		f, c = self.id[0]  # fila y columna del id de la pared
		p = self.id[1]  # posición reltiva del id de la pared

		if p == "N":
			pos_AI = ((f  , c  ), "O")
			pos_AC = ((f  , c-1), "N")
			pos_AD = ((f-1, c  ), "O")
			pos_BI = ((f-1, c+1), "O")
			pos_BC = ((f  , c+1), "N")
			pos_BD = ((f  , c+1), "O")

		elif p == "O":  
			pos_AI = ((f  , c-1), "N")
			pos_AC = ((f-1, c  ), "O")
			pos_AD = ((f  , c  ), "N")
			pos_BI = ((f+1, c  ), "N")
			pos_BC = ((f+1, c  ), "O")
			pos_BD = ((f+1, c-1), "N")

		res_continuaciones = {} 
		indice_paredes = self.__grid.index_paredes()

		if pos_AI in indice_paredes:  # Verifico que la pared exista
			res_continuaciones["AI"] = self.__grid.get_pared(pos_AI)
		else:  # Si no existe entonces es un borde y no hay continuación
			res_continuaciones["AI"] = None

		if pos_AC in indice_paredes:  # Verifico que la pared exista
			res_continuaciones["AC"] = self.__grid.get_pared(pos_AC)
		else:  # Si no existe entonces es un borde y no hay continuación
			res_continuaciones["AC"] = None

		if pos_AD in indice_paredes:  # Verifico que la pared exista
			res_continuaciones["AD"] = self.__grid.get_pared(pos_AD)
		else:  # Si no existe entonces es un borde y no hay continuación
			res_continuaciones["AD"] = None
		
		if pos_BI in indice_paredes:  # Verifico que la pared exista
			res_continuaciones["BI"] = self.__grid.get_pared(pos_BI)
		else:  # Si no existe entonces es un borde y no hay continuación
			res_continuaciones["BI"] = None
		
		if pos_BC in indice_paredes:  # Verifico que la pared exista
			res_continuaciones["BC"] = self.__grid.get_pared(pos_BC)
		else:  # Si no existe entonces es un borde y no hay continuación
			res_continuaciones["BC"] = None
		
		if pos_BD in indice_paredes:  # Verifico que la pared exista
			res_continuaciones["BD"] = self.__grid.get_pared(pos_BD)
		else:  # Si no existe entonces es un borde y no hay continuación
			res_continuaciones["BD"] = None

		return res_continuaciones

	def get_continuacion(self, posRel):
		'''Devuelve la pared continuación indicada en posRel. posRel
		es la posición relativa de la pared continuación, y es un 
		string que puede tomar cualquiera de los siguientes valores:

		"AI"  --> Es la continuación izquierda del vértice A
		"AC"  --> Es la continuación central del vértice A
		"AD"  --> Es la continuación derecha del vértice A
		"BI"  --> Es la continuación izquierda del vértice B
		"BC"  --> Es la continuación central del vértice B
		"BD"  --> Es la continuación derecha del vértice B

		Para definir si es continuación izquierda, central o derecha
		nos posicionamos sobre el vértice, dejando la pared a 
		nuestras espaldas. Delante nuestro tendremos las 
		continuaciones izquierda, central y derecha.'''


		return self.continuaciones()[posRel]

class _Vertice(object):
	"""Vértice de una celda. El id del vértice será el mismo que el
	de la celda ubicada en la posición SE.
	En caso de que el vértice no se pueda nombrar porque la celda 
	SE no existe, se procede igual que en el caso de las paredes,
	suponiendo una celda fantasma y nombrando al vértice relativo a
	ésta. Ésta celda fantasma realmente no existe y sirve solamente 
	para nombrar el vértice. """
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

		f, c = self.id  # fila y columna del id del vertice
		
		pos_N = ((f-1, c  ), "O")
		pos_E = ((f  , c  ), "N")
		pos_S = ((f  , c  ), "O")
		pos_O = ((f  , c-1), "N")

		indice_paredes = self.__grid.index_paredes()
		res_paredes = {}
		if pos_N in indice_paredes:  # Verifico que la pared exista
			res_paredes['N'] = self.__grid.get_pared(pos_N)
		else:  # Si no existe entonces es un borde
			res_paredes['N'] = None

		if pos_E in indice_paredes:  # Verifico que la pared exista
			res_paredes['E'] = self.__grid.get_pared(pos_E)
		else:  # Si no existe entonces es un borde
			res_paredes['E'] = None

		if pos_S in indice_paredes:  # Verifico que la pared exista
			res_paredes['S'] = self.__grid.get_pared(pos_S)
		else:  # Si no existe entonces es un borde
			res_paredes['S'] = None

		if pos_O in indice_paredes:  # Verifico que la pared exista
			res_paredes['O'] = self.__grid.get_pared(pos_O)
		else:  # Si no existe entonces es un borde
			res_paredes['O'] = None

		return res_paredes

	def get_pared(self, posRel):
		'''Devuelve la pared indicada en posRel. posRel es la posición 
		de la pared relativa al vértice, y es un string que puede 
		tomar cualquiera de los siguientes valores:
		
		"N" --> pared norte
		"E" --> pared este
		"S" --> pared sur
		"O" --> pared oeste
		
		Notar que si el vértice se encuentra en un borde, alguna de
		las paredes adyacentes será None, indicando que pertenece a
		una celda fantasma.'''

		return self.paredes()[posRel]

	def celdas(self):
		'''Devuelve un diccionario con las celdas adyacentes. La clave
		del diccionario es la posición relativa, y el valor la celda 
		adyacente en cuestión'''

		f, c = self.id[0]  # fila y columna del id del vertice

		pos_NO = (f-1, c-1)
		pos_NE = (f-1, c  )
		pos_SE = (f  , c  )
		pos_SO = (f  , c-1)

		indice_celdas = self.__grid.index_celdas()
		res_celdas = {}

		if pos_NO in indice_celdas:  # Verifico que la celda exista
			res_celdas['NO'] = self.__grid.get_celda(pos_NO)
		else:  # Si no existe entonces es un borde
			res_celdas['NO'] = None

		if pos_NE in indice_celdas:  # Verifico que la celda exista
			res_celdas['NE'] = self.__grid.get_celda(pos_NE)
		else:  # Si no existe entonces es un borde
			res_celdas['NE'] = None

		if pos_SE in indice_celdas:  # Verifico que la celda exista
			res_celdas['SE'] = self.__grid.get_celda(pos_SE)
		else:  # Si no existe entonces es un borde
			res_celdas['SE'] = None

		if pos_SO in indice_celdas:  # Verifico que la celda exista
			res_celdas['SO'] = self.__grid.get_celda(pos_SO)
		else:  # Si no existe entonces es un borde
			res_celdas['SO'] = None

		return res_celdas
	
	def get_celda(self, posRel):
		'''Devuelve la celda adyacente indicada en posRel. posRel es 
		la posición de la celda relativo al vértice, y es un string 
		que puede tomar cualquiera de los siguientes valores:
		
		"NO" --> celda noroeste
		"NE" --> celda noreste
		"SE" --> celda sudeste
		"SO" --> celda sudoeste

		Notar que si el vértice se encuentra en un borde, alguna de
		las celdas adyacentes será None, indicando que ésta es una 
		celda fantasma'''

		return self.celdas()[posRel]

