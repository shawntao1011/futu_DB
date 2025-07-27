Minutes:@[;`sym;`p#]
    ([] date        :0#0Nd;
        sym         :`;
        time        :0Np;
        name        :`;
        open        :0n;
        close       :0n;
        high        :0n;
        low         :0n;
        volume      :0n;
        turnover    :0n;
        kType       :`;
        lastClose   :0n;
        peRatio     :0n;
        turnoverRate:0n
    );
    
Ticks:@[;`sym;`p#]
    ([] date            :0#0Nd;
        sym             :`;
        time            :0Np;
        name            :`;
        price           :0n;
        volume          :0n;
        turnover        :0n;
        tickerDirection :`;
        sequence        :0Nj;
        tickType        :`;
        srcType         :`
    );


OrderBooks:@[;`sym;`p#]
    ([] date        :0#0Nd;
        sym         :`;
        time        :0Np;
        bidTime     :0Np;
        askTime     :0Np;
        ask1Price   :0n;
        ask2Price   :0n;
        ask3Price   :0n;
        ask4Price   :0n;
        ask5Price   :0n;
        ask6Price   :0n;
        ask7Price   :0n;
        ask8Price   :0n;
        ask9Price   :0n;
        ask10Price  :0n;
        ask1Volume  :0n;
        ask2Volume  :0n;
        ask3Volume  :0n;
        ask4Volume  :0n;
        ask5Volume  :0n;
        ask6Volume  :0n;
        ask7Volume  :0n;
        ask8Volume  :0n;
        ask9Volume  :0n;
        ask10Volume :0n;
        ask1qty     :0n;
        ask2qty     :0n;
        ask3qty     :0n;
        ask4qty     :0n;
        ask5qty     :0n;
        ask6qty     :0n;
        ask7qty     :0n;
        ask8qty     :0n;
        ask9qty     :0n;
        ask10qty    :0n;
        bid1Price   :0n;
        bid2Price   :0n;
        bid3Price   :0n;
        bid4Price   :0n;
        bid5Price   :0n;
        bid6Price   :0n;
        bid7Price   :0n;
        bid8Price   :0n;
        bid9Price   :0n;
        bid10Price  :0n;
        bid1Volume  :0n;
        bid2Volume  :0n;
        bid3Volume  :0n;
        bid4Volume  :0n;
        bid5Volume  :0n;
        bid6Volume  :0n;
        bid7Volume  :0n;
        bid8Volume  :0n;
        bid9Volume  :0n;
        bid10Volume :0n;
        bid1qty     :0n;
        bid2qty     :0n;
        bid3qty     :0n;
        bid4qty     :0n;
        bid5qty     :0n;
        bid6qty     :0n;
        bid7qty     :0n;
        bid8qty     :0n;
        bid9qty     :0n;
        bid10qty    :0n        
    );
    
FlatBrokerQs:@[;`sym;`p#]
    ([] date        :0#0Nd;
        sym         :`;
        time        :0Np;
        brokerID    :0n;
        brokerName  :`;
        brokerPos   :0n;
        orderID     :0n;
        orderVolume :0n;
        side        :`
    );
    
