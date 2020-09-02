
SOURCE_DIR="sets/int64/"
SET_DIR="sets/"


### int32sets
echo "Creating int32set from int64set..."
TARGET_DIR=$SET_DIR/int32/
# mkdir -p $TARGET_DIR
cp $SOURCE_DIR/int64set_header.pxi  $TARGET_DIR/int32set_header.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32set_header.pxi
cp $SOURCE_DIR/int64set_impl.pxi    $TARGET_DIR/int32set_impl.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32set_impl.pxi
cp $SOURCE_DIR/int64set_header_cpdef.pxi  $TARGET_DIR/int32set_header_cpdef.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32set_header_cpdef.pxi
cp $SOURCE_DIR/int64set_impl_cpdef.pxi    $TARGET_DIR/int32set_impl_cpdef.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32set_impl_cpdef.pxi
cp $SOURCE_DIR/int64set_impl_core.pxi    $TARGET_DIR/int32set_impl_core.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32set_impl_core.pxi


### float64set:
echo "Creating float64set from int64set..."
TARGET_DIR=$SET_DIR/float64/
# mkdir -p $TARGET_DIR
cp $SOURCE_DIR/int64set_header.pxi          $TARGET_DIR/float64set_header.pxi
sed -i -- 's/int64/float64/g'   $TARGET_DIR/float64set_header.pxi
sed -i -- 's/Int64/Float64/g'   $TARGET_DIR/float64set_header.pxi
cp $SOURCE_DIR/int64set_impl.pxi            $TARGET_DIR/float64set_impl.pxi
sed -i -- 's/int64/float64/g'   $TARGET_DIR/float64set_impl.pxi
sed -i -- 's/Int64/Float64/g'   $TARGET_DIR/float64set_impl.pxi
cp $SOURCE_DIR/int64set_header_cpdef.pxi          $TARGET_DIR/float64set_header_cpdef.pxi
sed -i -- 's/int64/float64/g'   $TARGET_DIR/float64set_header_cpdef.pxi
sed -i -- 's/Int64/Float64/g'   $TARGET_DIR/float64set_header_cpdef.pxi
cp $SOURCE_DIR/int64set_impl_cpdef.pxi            $TARGET_DIR/float64set_impl_cpdef.pxi
sed -i -- 's/int64/float64/g'   $TARGET_DIR/float64set_impl_cpdef.pxi
sed -i -- 's/Int64/Float64/g'   $TARGET_DIR/float64set_impl_cpdef.pxi
cp $SOURCE_DIR/int64set_impl_core.pxi            $TARGET_DIR/float64set_impl_core.pxi
sed -i -- 's/int64/float64/g'   $TARGET_DIR/float64set_impl_core.pxi
sed -i -- 's/Int64/Float64/g'   $TARGET_DIR/float64set_impl_core.pxi


### float32set:
echo "Creating float32set from float64set..."
SOURCE_DIR_FLOAT64=$SET_DIR/float64/
TARGET_DIR=$SET_DIR/float32/
# mkdir -p $TARGET_DIR
cp $SOURCE_DIR_FLOAT64/float64set_header.pxi          $TARGET_DIR/float32set_header.pxi
sed -i -- 's/64/32/g'             $TARGET_DIR/float32set_header.pxi
cp $SOURCE_DIR_FLOAT64/float64set_impl.pxi            $TARGET_DIR/float32set_impl.pxi
sed -i -- 's/64/32/g'             $TARGET_DIR/float32set_impl.pxi
cp $SOURCE_DIR_FLOAT64/float64set_header_cpdef.pxi          $TARGET_DIR/float32set_header_cpdef.pxi
sed -i -- 's/64/32/g'             $TARGET_DIR/float32set_header_cpdef.pxi
cp $SOURCE_DIR_FLOAT64/float64set_impl_cpdef.pxi            $TARGET_DIR/float32set_impl_cpdef.pxi
sed -i -- 's/64/32/g'             $TARGET_DIR/float32set_impl_cpdef.pxi
cp $SOURCE_DIR_FLOAT64/float64set_impl_core.pxi            $TARGET_DIR/float32set_impl_core.pxi
sed -i -- 's/64/32/g'             $TARGET_DIR/float32set_impl_core.pxi

### pyobjectset:
#
#  pyobjectset is special, so not everything can be copied...
#
SOURCE_DIR_FLOAT64=$SET_DIR/int64/
TARGET_DIR=$SET_DIR/pyobject/
echo "Partly creating pyobjectset from in64set..."
cp $SOURCE_DIR/int64set_header_cpdef.pxi          $TARGET_DIR/pyobjectset_header_cpdef.pxi
sed -i -- 's/_int64/_pyobject/g'   $TARGET_DIR/pyobjectset_header_cpdef.pxi
sed -i -- 's/Int64/PyObject/g'   $TARGET_DIR/pyobjectset_header_cpdef.pxi
sed -i -- 's/int64_t/object/g'   $TARGET_DIR/pyobjectset_header_cpdef.pxi
cp $SOURCE_DIR/int64set_impl_cpdef.pxi            $TARGET_DIR/pyobjectset_impl_cpdef.pxi
sed -i -- 's/_int64/_pyobject/g'   $TARGET_DIR/pyobjectset_impl_cpdef.pxi
sed -i -- 's/Int64/PyObject/g'   $TARGET_DIR/pyobjectset_impl_cpdef.pxi
sed -i -- 's/int64_t/object/g'   $TARGET_DIR/pyobjectset_impl_cpdef.pxi
cp $SOURCE_DIR/int64set_impl.pxi            $TARGET_DIR/pyobjectset_impl.pxi
sed -i -- 's/_int64/_pyobject/g'   $TARGET_DIR/pyobjectset_impl.pxi
sed -i -- 's/int64set/pyobjectset/g'   $TARGET_DIR/pyobjectset_impl.pxi
sed -i -- 's/Int64/PyObject/g'   $TARGET_DIR/pyobjectset_impl.pxi
sed -i -- 's/int64_t/object/g'   $TARGET_DIR/pyobjectset_impl.pxi


###  MAPS

SOURCE_DIR="maps/int64/"
MAP_DIR="maps/"


### int32map
echo "Creating int32map from int64map..."
TARGET_DIR=$MAP_DIR/int32/
# mkdir -p $TARGET_DIR
cp $SOURCE_DIR/int64to64map_header.pxi  $TARGET_DIR/int32to32map_header.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32to32map_header.pxi
cp $SOURCE_DIR/int64to64map_impl.pxi    $TARGET_DIR/int32to32map_impl.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/int32to32map_impl.pxi


### float64map
echo "Creating float64map from int64map..."
TARGET_DIR=$MAP_DIR/float64/
# mkdir -p $TARGET_DIR
cp $SOURCE_DIR/int64to64map_header.pxi  $TARGET_DIR/float64to64map_header.pxi
sed -i -- 's/ctypedef int64_t key_int64_t/ctypedef float64_t key_float64_t/g'   $TARGET_DIR/float64to64map_header.pxi
sed -i -- 's/key_int64_t/key_float64_t/g'   $TARGET_DIR/float64to64map_header.pxi
sed -i -- 's/int64to64/float64to64/g'   $TARGET_DIR/float64to64map_header.pxi
sed -i -- 's/Int64to64Map/Float64to64Map/g'   $TARGET_DIR/float64to64map_header.pxi
sed -i -- 's/_int64map/_float64map/g'   $TARGET_DIR/float64to64map_header.pxi
cp $SOURCE_DIR/int64to64map_impl.pxi    $TARGET_DIR/float64to64map_impl.pxi
sed -i -- 's/ctypedef int64_t key_int64_t/ctypedef float64_t key_float64_t/g'   $TARGET_DIR/float64to64map_impl.pxi
sed -i -- 's/key_int64_t/key_float64_t/g'   $TARGET_DIR/float64to64map_impl.pxi
sed -i -- 's/int64to64/float64to64/g'   $TARGET_DIR/float64to64map_impl.pxi
sed -i -- 's/Int64to64Map/Float64to64Map/g'   $TARGET_DIR/float64to64map_impl.pxi
sed -i -- 's/_int64map/_float64map/g'   $TARGET_DIR/float64to64map_impl.pxi



SOURCE_DIR="maps/float64/"

### float32map
echo "Creating float32map from float64map..."
TARGET_DIR=$MAP_DIR/float32/
# mkdir -p $TARGET_DIR
cp $SOURCE_DIR/float64to64map_header.pxi  $TARGET_DIR/float32to32map_header.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/float32to32map_header.pxi
cp $SOURCE_DIR/float64to64map_impl.pxi    $TARGET_DIR/float32to32map_impl.pxi
sed -i -- 's/64/32/g'   $TARGET_DIR/float32to32map_impl.pxi



