@.str = private constant [14 x i8] c"Hello World!\00\00", align 1

define i32 @main() ssp {
  %1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i32 0, i32 0))
  ret i32 0
}

declare i32 @printf(i8*, ...) #1

