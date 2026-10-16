def apply_discount(price, percent):
	"""할인이 적용된 가격을 돌려준다."""
	return int(price * (1 - percent / 100))
