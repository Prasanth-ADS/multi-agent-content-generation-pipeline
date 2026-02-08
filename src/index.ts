import { testConnection } from './lib/ollama-client';
import { logAgentExecution, generateRunId, printLogSummary } from './lib/logger';
import { countWords } from './lib/utils';

async function main() {
    console.log('\n');
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║                                                           ║');
    console.log('║      🚀 Content Pipeline - Ollama Local LLM Test          ║');
    console.log('║                                                           ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log('\n');

    // Test Ollama connection
    console.log('📡 Step 1: Testing Ollama connection...\n');

    const isConnected = await testConnection();

    if (!isConnected) {
        console.log('\n');
        console.log('╔═══════════════════════════════════════════════════════════╗');
        console.log('║  ❌ Ollama connection failed!                             ║');
        console.log('║                                                           ║');
        console.log('║  Please check:                                            ║');
        console.log('║  1. Ollama is installed: https://ollama.com               ║');
        console.log('║  2. Ollama is running: ollama serve                       ║');
        console.log('║  3. Model is pulled: ollama pull phi3                     ║');
        console.log('╚═══════════════════════════════════════════════════════════╝');
        console.log('\n');
        process.exit(1);
    }

    console.log('\n');
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║  ✅ Ollama connection successful!                         ║');
    console.log('║                                                           ║');
    console.log('║  Local LLM is ready for content generation!               ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log('\n');

    // Test logger
    console.log('📝 Step 2: Testing file-based logger...\n');

    const runId = generateRunId();
    console.log(`🆔 Generated Run ID: ${runId}\n`);

    // Simulate logging an agent execution
    await logAgentExecution(
        runId,
        'test-agent',
        'This is test input for the agent',
        {
            content: 'This is test output from the agent',
            metadata: {
                agent: 'test-agent',
                timestamp: new Date(),
            },
            success: true,
        }
    );

    // Test word count utility
    const sampleText = 'This is a sample text with ten words in it.';
    const wordCount = countWords(sampleText);
    console.log(`\n🔢 Word count test: "${sampleText}"`);
    console.log(`   Result: ${wordCount} words\n`);

    // Print log summary
    printLogSummary(runId);

    console.log('✅ All tests complete!');
    console.log('💡 Check the /logs directory for output files\n');

    console.log('🎉 Pipeline initialization complete!');
    console.log('📋 Available agents: Researcher, Writer, FactChecker, StylePolisher\n');
}

main().catch((error) => {
    console.error('💥 Pipeline failed to start:', error);
    process.exit(1);
});