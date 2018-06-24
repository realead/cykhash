
### int32set:
echo "Creating int32set from int64set..."
cp int64set_header.pxi  int32set_header.pxi
sed -i -- 's/64/32/g'   int32set_header.pxi
cp int64set_impl.pxi    int32set_impl.pxi
sed -i -- 's/64/32/g'   int32set_impl.pxi


### float64set:
echo "Creating float64set from int64set..."
cp int64set_header.pxi          float64set_header.pxi
sed -i -- 's/int64/float64/g'   float64set_header.pxi
sed -i -- 's/Int64/Float64/g'   float64set_header.pxi
cp int64set_impl.pxi            float64set_impl.pxi
sed -i -- 's/int64/float64/g'   float64set_impl.pxi
sed -i -- 's/Int64/Float64/g'   float64set_impl.pxi


### float32set:
echo "Creating float32set from float64set..."
cp float64set_header.pxi          float32set_header.pxi
sed -i -- 's/64/32/g'             float32set_header.pxi
cp float64set_impl.pxi            float32set_impl.pxi
sed -i -- 's/64/32/g'             float32set_impl.pxi

