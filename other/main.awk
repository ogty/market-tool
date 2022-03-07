BEGIN {
    OFS = ",";
    ORS = "";
}

# /.+,株式会社.+/ {
#     split($0, a, OFS);
#     data2["株式会社*****"] += 1;
# }

# /.+株式会社,.+/ {
#     split($0, a, OFS);
#     data2["*****株式会社"] += 1;
# }

{
    split($0, a, OFS);
    data[a[4]] += 1;
}

END {
    for (ip in data) {
        sum += data[ip];
    }

    for (ip in data) {
        tmp = sprintf("%d", (data[ip] / sum) * 100);
        printf("%2d%% - %s\n    |", int(tmp), ip);
        for (i = 0; i < int(tmp); i++) {
            printf "#";
        }
        print "\n";
    }

    # for (ip in data2) {
    #     sum2 += data2[ip];
    # }

    # for (ip in data2) {
    #     tmp = sprintf("%d", (data2[ip] / sum2) * 100);
    #     printf("%2d%% - %s\n    |", int(tmp), ip);
    #     for (i = 0; i < int(tmp); i++) {
    #         printf "#";
    #     }
    #     print "\n";
    # }
}
