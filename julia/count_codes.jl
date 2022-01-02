using CSV
using DataFrames


df = CSV.read("../data/data_j.csv", DataFrame)
df["コード"] = map(x -> string(x), df["コード"])
# TODO: 
codes = df[length(df["コード"]) .== 4, :]