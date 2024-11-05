DataTable.defaults.layout = {
    topStart: null,
    topEnd: null,
    bottomStart: null,
    bottomEnd: null
};

new DataTable('#employeeTable', {
    columnDefs: [
        {
            targets: 5,
            render: DataTable.render.datetime('Do MMM YYYY')
        }
    ],
    layout: {
        topEnd: 'search',
        bottom: ['info', 'pageLength', 'paging']
    }
});
