Minutes:@[;`sym;`p#]
    ([] time        :0#0Np;
        sym         :`;
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
    ([] time            :0#0Np;
        sym             :`;
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
    ([] time        :0#0Np;
        sym         :`;
        name        :`;
        level       :0Ni;
        bidTime     :0Np;
        bidPrice    :0n;
        bidVolume   :0n;
        bidqty      :0n;
        askTime     :0Np;
        askPrice    :0n;
        askVolume   :0n;
        askqty      :0n
    );

FlatBrokerQs:@[;`sym;`p#]
    ([] time        :0#0Np;
        sym         :`;
        name        :`;
        brokerID    :0Nj;
        brokerName  :`;
        brokerPos   :0Ni;
        orderID     :0Nj;
        orderVolume :0n;
        side        :`
    );
    
