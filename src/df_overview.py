# df_overviewモジュール
# 2018/5/11 yo16

import numpy as np
import pandas as pd
import copy

# df_overviewクラス
class df_overview(object):
	# 分析対象のDataFrame
	_df = None
	
	_debugMode = 1		# [ 0:release | 1:debug ]
	
	
	# -------------------------------------------
	# コンストラクタ
	# -------------------------------------------
	def __init__(self, df):
		self._df = copy.deepcopy(df)
		return
	
	
	# -------------------------------------------
	# 分析内容
	# -------------------------------------------
	# 列名
	def __anaName(self, c):
		return c
	
	# int か float か stringのいずれであるか調べる
	def __anaType(self, c):
		if isinstance(self._df[c].iat[0], np.int64):		# numpy.int64は、int?って聞くとFALSEと答えてしまう
			return 'int'
		if isinstance(self._df[c].iat[0], float):
			return 'float'
		return 'string'
		
	# 合計
	def __anaTotal(self, c):
		total = 0
		for i in range(len(self._df)):
			total = total + self._df[c][i]
		
		return total
	def __anaMean(self, c):
		return 0	# めんどくさいので未実装
	# 最小値
	def __anaMin(self, c):
		min = 0
		for i in range(len(self._df)):
			if self._df[c][i] < min:
				min = self._df[c][i]
		return min
	# 最大値
	def __anaMax(self, c):
		max = 0
		for i in range(len(self._df)):
			if max < self._df[c][i]:
				max = self._df[c][i]
		return max
	# ユニークな種類数
	def __anaKind(self, c):
		return len(self._df[c].unique())
	# ユニークな種類の上位
	def __anaUniqueTop(self, c, n):
		vc = self._df[c].value_counts(dropna=False)		# NaNも加算
		vc = vc[:n]
		# dict型に整形してあげる
		d = {}
		for i, v in vc.iteritems():
			 d[i] = v
		return d
		
	# 型
	# 合計(*)
	# 平均(*)
	# 最小値(*)
	# 最大値(*)
	# 値の種類数
	# (*):数値型のときのみ
	_ANALYZE_METHOD = {	\
		'name':		__anaName		\
	,	'type':		__anaType		\
	,	'total':	__anaTotal		\
	,	'mean':		__anaMean		\
	,	'min':		__anaMin		\
	,	'max':		__anaMax		\
	,	'kind':		__anaKind		\
	,	'unique':	__anaUniqueTop	\
	}
	
	
	# -------------------------------------------
	# _dfの列のサマリのDataFrameを返す
	# -------------------------------------------
	def cols_summary(self):
		# 列数
		self.__debugPrint('shape:(%d,%d)' % self._df.shape)
		
		# 戻り値のDataFrame
		dfRet = pd.DataFrame()
		
		# １列ごとにサマって、dfへ結合していく
		# 元情報の１列＝１行
		for c in self._df.columns:
			self.__debugPrint(c)
			dfRet = pd.concat([dfRet,self.__summary_one_column(c)])
		
		# 列を並び替える
		dfRet = dfRet[['列名','型','合計','平均','最小値','最大値','種類数','ユニーク上位']]
		
		return dfRet
	
	
	# -------------------------------------------
	# １列のサマリを得る
	# -------------------------------------------
	def __summary_one_column(self, columnName):
		
		dictData = {}
		isNum = False
		lineNum = len(self._df)
		
		# 集計
		# 列名
		dictData['列名'] = [self._ANALYZE_METHOD['name'](self, columnName)]
		# 型
		dictData['型']   = [self._ANALYZE_METHOD['type'](self, columnName)]
		isNum = (dictData['型'][0] != 'string')
		# 合計
		dictData['合計'] = [self._ANALYZE_METHOD['total'](self, columnName)] if isNum else 0
		# 平均
		dictData['平均'] = dictData['合計'][0] / lineNum if isNum else 0
		# 最小
		dictData['最小値'] = [self._ANALYZE_METHOD['min'](self, columnName)] if isNum else 0
		# 最大
		dictData['最大値'] = [self._ANALYZE_METHOD['max'](self, columnName)] if isNum else 0
		# 種類数
		dictData['種類数'] = [self._ANALYZE_METHOD['kind'](self, columnName)]
		# ユニーク上位
		dictData['ユニーク上位'] = [self._ANALYZE_METHOD['unique'](self, columnName, 10)]
		
		df = pd.DataFrame(dictData)
		
		return df
	
	
	# -------------------------------------------
	# デバッグ用print
	# -------------------------------------------
	def __debugPrint(self, str):
		if self._debugMode == 1:
			print(str)
		return


