#include <stdio.h> 

double y = 1 ;

void fact(double x) {
	if (x > 0)
	{
		y = y * x ;
		fact(x - 1) ;
	}
}

int main(void) {
	fact(100) ;
	printf("%f\n", y) ;
}


