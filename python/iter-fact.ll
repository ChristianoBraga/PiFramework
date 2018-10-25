
; ModuleID = "main_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define i64 @"main_function"() 
{
entry:
  %"ptr" = alloca i64
  store i64 1, i64* %"ptr"
  %"ptr.1" = alloca i64
  store i64 10, i64* %"ptr.1"
  br label %"loop"
loop:
  %"val" = load i64, i64* %"ptr.1"
  %"temp_eq" = icmp eq i64 %"val", 0
  %"temp_not" = xor i1 %"temp_eq", -1
  %"val.1" = load i64, i64* %"ptr"
  %"val.2" = load i64, i64* %"ptr.1"
  %"tmp_mul" = mul i64 %"val.1", %"val.2"
  store i64 %"tmp_mul", i64* %"ptr"
  %"val.3" = load i64, i64* %"ptr.1"
  %"tmp_sub" = sub i64 %"val.3", 1
  store i64 %"tmp_sub", i64* %"ptr.1"
  br i1 %"temp_not", label %"loop", label %"after_loop"
after_loop:
  ret i64 0
}

