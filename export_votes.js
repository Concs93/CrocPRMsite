// Script para exportar votos do localStorage
// Cole isso no Console do navegador (F12) para exportar seus votos

(function() {
    const votes = [];
    const allKeys = Object.keys(localStorage);
    
    // Coleta todos os votos do localStorage
    allKeys.forEach(key => {
        if (key.startsWith('luna_user_vote_')) {
            const itemName = key.replace('luna_user_vote_', '');
            const voteType = localStorage.getItem(key);
            
            if (voteType) {
                votes.push({
                    timestamp: new Date().toISOString(),
                    item_name: itemName,
                    vote_type: voteType,
                    action: 'add'
                });
            }
        }
    });
    
    // Cria arquivo JSON para download
    const dataStr = JSON.stringify(votes, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `luna_votes_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    console.log('✅ Votos exportados!', votes.length, 'votos encontrados');
    console.log('📋 Dados:', votes);
})();
