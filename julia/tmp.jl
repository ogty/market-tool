using CSV
using DataFrames


df = CSV.read("../data/data_j.csv", DataFrame)
codes = df["コード"]
println(length(codes))

for code in codes
    if 6000 < code < 6100
        println(code)
    end
end