@y = global double 1.000000e+00 
@.str = private constant [4 x i8] c"%f\0A\00"

define void @_Z4factd(double) {
  %2 = alloca double, align 8
  store double %0, double* %2
  %3 = load double, double* %2
  %4 = fcmp ogt double %3, 0.000000e+00
  br i1 %4, label %5, label %11

; <label>:5:                                     
  %6 = load double, double* @y
  %7 = load double, double* %2
  %8 = fmul double %6, %7
  store double %8, double* @y
  %9 = load double, double* %2
  %10 = fsub double %9, 1.000000e+00
  call void @_Z4factd(double %10)
  br label %11

; <label>:11:                                     
  ret void
}

define i32 @main() {
  call void @_Z4factd(double 1.000000e+02)
  %1 = load double, double* @y
  %2 = call i32 (i8*, ...) 
       @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), double %1)
  ret i32 0
}

declare i32 @printf(i8*, ...) 

