colours=[["#660000","#863030","#ba4a4a","#de7e7e","#ffaaaa"],["#a34b00","#d46200","#ff7a04","#ff9b42","#fec28d"],["#dfd248","#fff224","#eefd5d","#f5ff92","#f9ffbf"],["#006600","#308630","#4aba4a","#7ede7e","#aaffaa"]]
c = "#863030"
x = [(i, colour.index("#863030")) for i, colour in enumerate(colours) if "#863030" in colours]
print(x)
