
char bar(char d, char e) {
	return d - e;
}

char foo(int a, char b, int c) {
	return a + bar(b + c, 4);
}

void main() {
	char d = foo(1,2,3);
	d = d + bar(d, 4);
}
