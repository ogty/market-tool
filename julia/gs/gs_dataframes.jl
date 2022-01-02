using CSV
using DataFrames


# Commenting out may be a comparison with Python

df = CSV.read("../../data/data_j.csv", DataFrame)

codes = df["コード"]
println(typeof(codes)) # Vector{Int64}

columns = names(df)    # columns
df_size = size(df)     # shape

println(first(df, 5))  # head
println(last(df, 5))   # tail

search_code = 7974
company_name = df[df["コード"] .== search_code, :]["銘柄名"]
# first method or index
println(typeof(company_name)) # Vector{String}
println(first(company_name))  # 任天堂

# multiple conditions
# note: .&
search_market = "市場第一部（内国株）"
company_name = df[(df["コード"] .> 9900) .& (df["市場・商品区分"] .== search_market), :]["銘柄名"]