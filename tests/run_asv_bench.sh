cd asv_bench

# Examples:
#
# Run all:
# python -m asv -f 1.01 upstream/master HEAD 
#
# Only from file 
#python -m asv continuous -f 1.01 upstream/master HEAD -b ^count_if
#
# Only classes (which starts with something) from files:
# python -m asv continuous -f 1.01 upstream/master HEAD -b ^count_if.CountIf -b ^set_methods.CreateArange


python -m asv continuous -f 1.01 HEAD~1 HEAD
