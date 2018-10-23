	.text
	.file	"iter-fact.ll"
	.globl	main_function           # -- Begin function main_function
	.p2align	4, 0x90
	.type	main_function,@function
main_function:                          # @main_function
	.cfi_startproc
# %bb.0:                                # %entry
	movq	$1, -8(%rsp)
	movq	$10, -16(%rsp)
	.p2align	4, 0x90
.LBB0_1:                                # %loop
                                        # =>This Inner Loop Header: Depth=1
	movq	-16(%rsp), %rax
	movq	-8(%rsp), %rcx
	imulq	%rax, %rcx
	testq	%rax, %rax
	leaq	-1(%rax), %rax
	movq	%rcx, -8(%rsp)
	movq	%rax, -16(%rsp)
	jne	.LBB0_1
# %bb.2:                                # %after_loop
	xorl	%eax, %eax
	retq
.Lfunc_end0:
	.size	main_function, .Lfunc_end0-main_function
	.cfi_endproc
                                        # -- End function

	.section	".note.GNU-stack","",@progbits
