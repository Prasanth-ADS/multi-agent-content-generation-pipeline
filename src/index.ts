import dotenv from 'dotenv';
import { testConnection } from './lib/openai-client';
import logger from './lib/logger';

// Load environment variables
dotenv.config();

async function main() {
    console.log('\n');
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║                                                           ║');
    console.log('║      🚀 Content Pipeline Starting                         ║');
    console.log('║                                                           ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log('\n');

    // Confirm TypeScript is working
    const timestamp: string = new Date().toISOString();
    logger.info(`TypeScript is working! Current time: ${timestamp}`);

    // Test OpenAI connection
    console.log('\n📡 Step 1: Testing OpenAI API connection...\n');

    const isConnected = await testConnection();

    if (!isConnected) {
        console.log('\n');
        console.log('╔═══════════════════════════════════════════════════════════╗');
        console.log('║  ❌ OpenAI connection failed!                             ║');
        console.log('║                                                           ║');
        console.log('║  Please check:                                            ║');
        console.log('║  1. Your .env file has OPENAI_API_KEY=sk-...              ║');
        console.log('║  2. Your API key is valid and has credits                 ║');
        console.log('║  3. You have internet connection                          ║');
        console.log('╚═══════════════════════════════════════════════════════════╝');
        console.log('\n');
        process.exit(1);
    }

    console.log('\n');
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║  ✅ OpenAI connection successful!                         ║');
    console.log('║                                                           ║');
    console.log('║  Pipeline is ready for content generation!                ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log('\n');

    // Display available agents
    logger.info('Available agents:', {
        agents: ['Researcher', 'Writer', 'FactChecker', 'StylePolisher']
    });

    logger.info('🎉 Pipeline initialization complete!');
}

main().catch((error) => {
    logger.error('💥 Pipeline failed to start', error);
    process.exit(1);
});
